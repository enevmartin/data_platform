# apps/core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.core.models import DataFile
from apps.core.processors.factory import get_processor_for_filetype

## Fix for signals.py
@receiver(post_save, sender=DataFile)
def process_datafile(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        # Trigger processing asynchronously
        try:
            processor = get_processor_for_filetype(instance.file_type)
            if processor:
                from apps.core.tasks import process_file_task
                process_file_task.delay(instance.id)
            else:
                # Update status to failed if no processor is found
                instance.status = 'failed'
                instance.save(update_fields=['status'])
        except Exception as e:
            # Log the error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error processing file {instance.id}: {str(e)}")
            # Update status
            instance.status = 'failed'
            instance.save(update_fields=['status'])