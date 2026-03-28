from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = HTMLField()

    # External URLs for PythonAnywhere efficiency
    featured_image_url = models.URLField(max_length=500, blank=True, help_text="Paste an image URL from Pinterest, Imgur, etc.")
    video_url = models.URLField(max_length=500, blank=True, help_text="Link to YouTube/Vimeo")

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Using TaggableManager exclusively
    tags = TaggableManager()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

class LegalPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Use 'terms' or 'privacy'")
    content = HTMLField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SystemStatus(models.Model):
    MOOD_CHOICES = [
        ('clear', '1. Clear'),
        ('cloud', '2. Cloud'),
        ('rain', '3. Rain'),
        ('storm', '4. Storm'),
        ('fog', '5. Fog'),
        ('glitch', '6. Glitch'),
    ]
    active_mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='clear')

    class Meta:
        verbose_name_plural = "System Status"

    def __str__(self):
        return f"Global System Mood: {self.active_mood}"