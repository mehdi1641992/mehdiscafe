from django.contrib import admin
from .models import Category, Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at')
    
    fieldsets = (
        ('Main Editor', {
            'fields': ('title', 'content'),
            'classes': ('main-column',), 
        }),
        ('Post Settings', {
            # UPDATED: We swapped 'image' for 'featured_image_url' here
            'fields': ('category', 'tags', 'featured_image_url', 'video_url', 'is_featured'),
            'classes': ('sidebar-column',),
        }),
    )

    class Media:
        css = {
            'all': ('css/modern_admin.css',)
        }

admin.site.register(Category)
admin.site.register(Comment)