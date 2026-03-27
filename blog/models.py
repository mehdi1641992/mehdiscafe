from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    content = HTMLField()

    # NEW: External URLs instead of direct uploads
    featured_image_url = models.URLField(max_length=500, blank=True, help_text="Paste an image URL from Pinterest, Imgur, etc.")
    video_url = models.URLField(max_length=500, blank=True, help_text="Link to YouTube/Vimeo")

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)