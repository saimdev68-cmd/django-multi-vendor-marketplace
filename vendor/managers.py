from .querysets import VendorQuerySet
from django.db import models

class VendorManager(models.Manager):

    def get_queryset(self):
        return VendorQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def featured(self):
        return self.get_queryset().featured()
    
    def active_featured(self):
        return self.get_queryset().active_featured()