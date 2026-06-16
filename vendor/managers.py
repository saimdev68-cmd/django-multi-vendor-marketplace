from django.db import models
from .querysets import VendorQuerySet

VendorManager = models.Manager.from_queryset(VendorQuerySet)