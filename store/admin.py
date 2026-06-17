from django.contrib import admin
from .models import Country , City

# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", 'id',"country_code", "currency_code", "phone_prefix", "is_active")
    list_editable = ("is_active",)
    search_fields = ("name", "country_code")
    ordering = ["name"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_active")
    list_editable = ("is_active",)
    list_filter = ("country", "is_active")
    search_fields = ("name", "country__name")
    ordering = ["country", "name"]