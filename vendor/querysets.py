from django.db import models

class VendorQuerySet(models.QuerySet):

    def with_detail(self):
        return self.select_related('city','country','owner')

    def active(self):
        return self.filter(status='active')
    
    def featured(self):
        return self.filter(is_featured=True)
    
    def active_featured(self):
        return self.featured().active()