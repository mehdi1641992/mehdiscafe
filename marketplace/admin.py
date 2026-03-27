from django.contrib import admin
from .models import Product, ProductImage, WebringSite

# This embeds the extra images directly inside the Product edit page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5 # Shows 5 empty rows by default

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline] # Attaches the gallery to the product
    list_display = ('name', 'price_display', 'is_active')

@admin.register(WebringSite)
class WebringSiteAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_url', 'approved')
    list_filter = ('approved',)