from django.db import models
from tinymce.models import HTMLField # This enables the rich text editor!

class Product(models.Model):
    name = models.CharField(max_length=200)
    # The primary image shown in the Bazaar list
    image_url = models.URLField(max_length=500, help_text="Cover Image URL") 
    
    # Changed from TextField to HTMLField for blog-style formatting
    description = HTMLField() 
    
    external_link = models.URLField(help_text="Link to Amazon/Gumroad/etc.")
    price_display = models.CharField(max_length=50, help_text="e.g. $9.99 or FREE")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# NEW: This allows adding infinite extra images to a single product
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500, help_text="Additional Image URL")

    def __str__(self):
        return f"Image for {self.product.name}"

class WebringSite(models.Model):
    site_name = models.CharField(max_length=200)
    site_url = models.URLField()
    description = models.CharField(max_length=255)
    approved = models.BooleanField(default=False, help_text="Check this to display it on the site")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name