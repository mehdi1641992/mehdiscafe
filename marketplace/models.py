from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField(max_length=500, help_text="Image URL from Pinterest, Imgur, etc.")
    description = models.TextField()
    external_link = models.URLField(help_text="Link to Amazon/Gumroad/etc.")
    price_display = models.CharField(max_length=50, help_text="e.g. $9.99 or FREE")
    is_active = models.BooleanField(default=True)

    def __str__(self): 
        return self.name

class WebringSite(models.Model):
    site_name = models.CharField(max_length=200)
    site_url = models.URLField()
    description = models.CharField(max_length=255)
    approved = models.BooleanField(default=False, help_text="Check this to display it on the site")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.site_name