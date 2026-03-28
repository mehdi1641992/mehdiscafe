from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Comment, LegalPage
from taggit.models import Tag
import random

def post_list(request):
    # 1. Capture GET parameters
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    year_filter = request.GET.get('year', '')
    month_filter = request.GET.get('month', '')
    tag_ids = request.GET.getlist('tags')

    # 2. Base Queryset (Latest to Oldest)
    all_posts = Post.objects.all().order_by('-created_at')

    # Check if any filter is actively applied
    is_filtered = bool(query or category_id or year_filter or month_filter or tag_ids)

    # 3. Apply Filters sequentially
    if query:
        all_posts = all_posts.filter(title__icontains=query)
    if category_id:
        all_posts = all_posts.filter(category_id=category_id)
    if year_filter:
        all_posts = all_posts.filter(created_at__year=year_filter)
    if month_filter:
        all_posts = all_posts.filter(created_at__month=month_filter)
    if tag_ids:
        all_posts = all_posts.filter(tags__id__in=tag_ids).distinct()

    # 4. Carousel Logic
    featured_carousel = []

    if not is_filtered:
        # Grabs ONLY the newest featured post
        featured_main = Post.objects.filter(is_featured=True).order_by('-created_at').first()
        exclude_ids = [featured_main.id] if featured_main else []

        # Grabs the 3 latest posts (excluding the featured one so it doesn't show twice in the carousel)
        latest_three = Post.objects.exclude(id__in=exclude_ids).order_by('-created_at')[:3]

        if featured_main:
            featured_carousel.append(featured_main)

        featured_carousel.extend(list(latest_three))

        # REMOVED the code that excluded these from all_posts!
        # Now they will show up in the grid below as well.

    # 5. Pagination
    paginator = Paginator(all_posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 6. Gather Filter Options for the Modal UI
    categories = Category.objects.all()
    tags = Tag.objects.all()
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
        'categories': categories,
        'tags': tags,
        'years': years,
        'months': months,
        'current_q': query,
        'current_cat': int(category_id) if category_id.isdigit() else '',
        'current_year': int(year_filter) if year_filter.isdigit() else '',
        'current_month': int(month_filter) if month_filter.isdigit() else '',
        'current_tags': [int(t) for t in tag_ids if t.isdigit()],
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id).order_by('?')[:3]
    # Fetch all approved comments for this specific post
    comments = post.comments.filter(is_approved=True).order_by('-created_at')

    if related_posts.count() < 3:
        latest_fallback = Post.objects.exclude(id=post.id).exclude(id__in=[p.id for p in related_posts]).order_by('-created_at')[:3 - related_posts.count()]
        related_posts = list(related_posts) + list(latest_fallback)

    # Handle the comment form submission
    if request.method == 'POST':
        author = request.POST.get('author')
        body = request.POST.get('body')

        if author and body:
            Comment.objects.create(post=post, author=author, body=body)
            # Refresh the page to show the new comment
            return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments
    })

def legal_page(request, slug):
    # Fetch the page from the database
    page = get_object_or_404(LegalPage, slug=slug)
    # Dynamically render templates/legal/terms.html OR templates/legal/privacy.html
    return render(request, f'legal/{slug}.html', {'page': page})