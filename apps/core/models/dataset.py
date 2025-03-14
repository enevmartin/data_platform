# apps/core/models/dataset.py
from django.db import models
from .base_models import TimeStampedModel
from .mixins import SoftDeletableMixin
from .managers import DatasetManager, DatasetQuerySet


class Dataset(TimeStampedModel, SoftDeletableMixin):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    institution = models.ForeignKey(
        'Institution',
        on_delete=models.CASCADE,
        related_name='datasets'
    )
    is_active = models.BooleanField(default=True)

    # Add custom manager
    objects = DatasetManager.from_queryset(DatasetQuerySet)()

    class Meta:
        indexes = [
            models.Index(fields=['name', 'institution']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name