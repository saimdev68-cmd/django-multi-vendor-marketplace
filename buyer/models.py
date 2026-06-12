from django.db import models
from accounts.models import User


class Buyer(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="buyer")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to="buyers/profiles/",default="default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.username