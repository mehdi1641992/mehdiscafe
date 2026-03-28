from django.contrib import admin
from .models import Post, Category, Comment, LegalPage, SystemStatus

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_featured')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content')

# 1. The Comment Admin (Only registered ONCE)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author', 'body')

# 2. The Legal Page Admin
@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SystemStatus)
class SystemStatusAdmin(admin.ModelAdmin):
    # Update this list to ONLY include the field currently in your model
    list_display = ('active_mood',)