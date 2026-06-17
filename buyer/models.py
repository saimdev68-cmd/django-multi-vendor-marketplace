from django.db import models
from accounts.models import User 
from django.core.validators import RegexValidator

def buyer_profile_path(instance,filename):
    ext = filename.split('.')[-1].lower()
    buyer_id = instance.id if instance.id else 0
    return f"buyer/{buyer_id}/profile.{ext}"

class Buyer(models.Model):
    
    phone_validation = RegexValidator(
        regex=r"^\+?[1-9]\d{8-14}$",
        message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed."
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="buyer")
    phone_number = models.CharField(max_length=17,validators=[phone_validation],blank=True, null=True)
    profile_image = models.ImageField(upload_to=buyer_profile_path,default="default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"
        db_table = "buyers"
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Buyer Profile: {self.user.email}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)