from django.contrib import admin
from .models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "release_date", "lte_exists", "slug")
    search_fields = ("name", "slug")
    list_filter = ("lte_exists",)