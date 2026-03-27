from django.shortcuts import render, get_object_or_404
from .models import Post, Category

def post_list(request):
    # Grab the latest featured post
    featured_post = Post.objects.filter(is_featured=True).order_by('-created_at').first()
    
    # Grab all other posts (excluding the featured one so it doesn't duplicate)
    if featured_post:
        posts = Post.objects.exclude(id=featured_post.id).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
        
    return render(request, 'blog/post_list.html', {
        'featured_post': featured_post,
        'posts': posts
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})