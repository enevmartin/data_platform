# apps/core/models/managers.py
from django.db import models


class DatasetQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def by_institution(self, institution_id):
        return self.filter(institution_id=institution_id)


class DatasetManager(models.Manager):
    def get_queryset(self):
        return DatasetQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()