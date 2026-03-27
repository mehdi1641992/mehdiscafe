from django.contrib import admin
from .models import Product, WebringSite

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display', 'is_active')
    list_filter = ('is_active',)

@admin.register(WebringSite)
class WebringSiteAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_url', 'approved', 'created_at')
    list_filter = ('approved',)