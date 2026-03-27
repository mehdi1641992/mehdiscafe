from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag  # <-- Added Tag here!

def post_list(request):
    # 1. Capture GET parameters
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    year_filter = request.GET.get('year', '')
    month_filter = request.GET.get('month', '')
    tag_ids = request.GET.getlist('tags') # Gets a list of selected tag IDs

    # 2. Base Queryset (Latest to Oldest)
    all_posts = Post.objects.all().order_by('-created_at')

    # Check if any filter is actively applied
    is_filtered = bool(query or category_id or year_filter or month_filter or tag_ids)

    # 3. Apply Filters sequentially
    if query:
        # Search ONLY in the title as requested
        all_posts = all_posts.filter(title__icontains=query)
    if category_id:
        all_posts = all_posts.filter(category_id=category_id)
    if year_filter:
        all_posts = all_posts.filter(created_at__year=year_filter)
    if month_filter:
        all_posts = all_posts.filter(created_at__month=month_filter)
    if tag_ids:
        # Show posts that contain ANY of the selected tags
        all_posts = all_posts.filter(tags__id__in=tag_ids).distinct()
    
    # 4. Carousel Logic (Hide if user is searching/filtering)
    featured_carousel = []
    if not is_filtered:
        featured_main = Post.objects.filter(is_featured=True).order_by('-created_at').first()
        exclude_ids = [featured_main.id] if featured_main else []
        latest_three = Post.objects.exclude(id__in=exclude_ids).order_by('-created_at')[:3]
        
        if featured_main:
            featured_carousel.append(featured_main)
        featured_carousel.extend(list(latest_three))
        
        # Remove carousel items from the grid below
        carousel_ids = [p.id for p in featured_carousel]
        all_posts = all_posts.exclude(id__in=carousel_ids)

    # 5. Pagination: 12 posts per page
    paginator = Paginator(all_posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 6. Gather Filter Options for the Modal UI
    categories = Category.objects.all()
    tags = Tag.objects.all()
    # Extract unique years from the database
    dates = Post.objects.dates('created_at', 'year', order='DESC')
    years = [d.year for d in dates]
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    context = {
        'page_obj': page_obj,
        'featured_posts': featured_carousel,
        'is_filtered': is_filtered,
        
        # UI Options
        'categories': categories,
        'tags': tags,
        'years': years,
        'months': months,
        
        # Currently selected values (to keep inputs populated)
        'current_q': query,
        'current_cat': int(category_id) if category_id.isdigit() else '',
        'current_year': int(year_filter) if year_filter.isdigit() else '',
        'current_month': int(month_filter) if month_filter.isdigit() else '',
        'current_tags': [int(t) for t in tag_ids if t.isdigit()],
    }
    return render(request, 'blog/post_list.html', context)

# ENSURE THIS IS AT THE BOTTOM AND NOT INDENTED
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})