from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category

def post_list(request):
    # 1. Search Logic
    query = request.GET.get('q')
    
    # 2. Carousel Logic: 1 Featured + 3 Latest
    # We grab the latest post marked as featured
    featured_main = Post.objects.filter(is_featured=True).order_by('-created_at').first()
    
    # Exclude it from the next query to avoid duplicates
    exclude_ids = [featured_main.id] if featured_main else []
    latest_three = Post.objects.exclude(id__in=exclude_ids).order_by('-created_at')[:3]
    
    # Combine for the carousel
    featured_carousel = []
    if featured_main:
        featured_carousel.append(featured_main)
    featured_carousel.extend(list(latest_three))
    
    # Update exclude list for the grid
    exclude_ids.extend([p.id for p in latest_three])

    # 3. Grid Logic: All other posts
    all_grid_posts = Post.objects.exclude(id__in=exclude_ids).order_by('-created_at')

    if query:
        all_grid_posts = all_grid_posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # 4. Pagination: 12 posts per page
    paginator = Paginator(all_grid_posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'featured_posts': featured_carousel,
        'page_obj': page_obj,
        'query': query
    })

# ENSURE THIS IS AT THE BOTTOM AND NOT INDENTED
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})