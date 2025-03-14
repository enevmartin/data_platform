from .institution import Institution
# from .dataset import Dataset
from .data_file import DataFile, ProcessedData

__all__ = ['Institution', 'DataFile', 'ProcessedData']

# 'Dataset'


# apps/core/models/base_models.py
from django.db import models

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides
    self-updating created and modified fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


