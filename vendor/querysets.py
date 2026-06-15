from django.db import models

class VendorQuerySet(models.QuerySet):

    def active(self):
        return self.filter(status='active')
    
    def featured(self):
        return self.filter(is_featured=True)
    
    def active_featured(self):
        return self.active().featured()