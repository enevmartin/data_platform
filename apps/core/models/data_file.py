from django.db import models
import uuid
import os


def file_upload_path(instance, filename):
    """Generate a unique path for uploaded files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', str(instance.dataset.id), filename)


class DataFile(models.Model):
    """
    Represents a data file within a dataset.
    """
    FILE_TYPE_CHOICES = (
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('pdf', 'PDF'),
        ('parquet', 'Parquet'),
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('validated', 'Validated'),
        ('error', 'Error'),
        ('processed', 'Processed'),
    )

    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=file_upload_path)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    size_bytes = models.BigIntegerField(default=0)
    md5_hash = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file_name

    def save(self, *args, **kwargs):
        if self.file and not self.size_bytes:
            self.size_bytes = self.file.size
        super().save(*args, **kwargs)


class ProcessedData(models.Model):
    """
    Represents processed data derived from a data file.
    """
    data_file = models.ForeignKey('DataFile', on_delete=models.CASCADE, related_name='processed_data')
    output_file = models.FileField(upload_to='processed/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(default=0.0)  # Time in seconds
    processing_metadata = models.JSONField(default=dict, blank=True)
    quality_score = models.FloatField(default=0.0)
    row_count = models.IntegerField(default=0)
    validation_results = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Processed data for {self.data_file.file_name}"