from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Country(models.Model):

    name = models.CharField(max_length=200 , unique=True)
    country_code = models.CharField(max_length=10 , unique=True)
    currency_code = models.CharField(max_length=3, default="USD", help_text="ISO currency code (e.g., USD, EUR)")
    phone_prefix = models.CharField(max_length=7, blank=True, help_text="International phone prefix (e.g., +1 or +92)")
    is_active = models.BooleanField(default=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]
        db_table = "countries"

    def __str__(self):
        return self.name
    
class City(models.Model):

    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="cities")

    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True , db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name},{self.country.name}"
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ("country",'name')
        ordering = ["name"]
        db_table = "cities"
        indexes = [ 
            models.Index(fields=["country",'is_active'])
        ]

class Currency(models.Model):
    
    name = models.CharField(max_length=50,unique=True)
    code = models.CharField(max_length=3,unique=True)
    is_active = models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name},{self.code}"
    
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = "Currencies"
        db_table = "currencies"
        ordering = ['name']

class Bank(models.Model):

    name = models.CharField(max_length=255, unique=True)
    country_iso_code = models.CharField(
        max_length=4, 
        blank=True, 
        null=True,
        help_text="The 2 or 3-letter country code prefix (e.g., US, GB, PK)."
    )
    swift_code = models.CharField(
        max_length=11,
        unique=True,
        validators=[MinLengthValidator(8)],
        help_text="Standardized Business Identifier Code (BIC) - must be exactly 8 or 11 characters."
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Toggle off to completely block vendors from linking accounts to this bank."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "banks"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.swift_code})"
