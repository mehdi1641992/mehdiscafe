from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail     # <--- ADD THIS
from django.contrib import messages        # <--- ADD THIS
from django.conf import settings           # <--- ADD THIS
from blog.models import Post
from marketplace.models import Product
from blog import views as blog_views
import os


# The Boot Screen
def intro(request):
    return render(request, 'intro.html')

# The Actual Home Page
def home(request):
    latest_posts = Post.objects.all().order_by('-created_at')[:4]  # Fetch 4 posts
    featured_products = Product.objects.filter(is_active=True)[:4] # Fetch 4 products

    return render(request, 'home.html', {
        'posts': latest_posts,
        'products': featured_products
    })

# Add these new simple views to your urls.py
def privacy(request):
    return render(request, 'legal/privacy.html')

def terms(request):
    return render(request, 'legal/terms.html')

def sitemap(request):
    # This generates a basic XML sitemap on the fly
    posts = Post.objects.all()
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

    # Static Pages
    pages = ['', '/home/', '/blog/', '/marketplace/', '/contact/', '/privacy/']
    for page in pages:
        xml_content += f'<url><loc>https://mehdimchow.pythonanywhere.com{page}</loc><changefreq>weekly</changefreq></url>'

    # Dynamic Blog Posts
    for post in posts:
        xml_content += f'<url><loc>https://mehdimchow.pythonanywhere.com/blog/{post.id}/</loc><lastmod>{post.created_at.strftime("%Y-%m-%d")}</lastmod></url>'

    xml_content += '</urlset>'
    return HttpResponse(xml_content, content_type="application/xml")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Message from {name} ({email}):\n\n{message}"

        try:
            send_mail(
                f"CAFE_MSG: {subject}",
                full_message,
                settings.EMAIL_HOST_USER,
                ['mmc1641992@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "TRANSMISSION SUCCESSFUL. DATA LOGGED.")
        except Exception as e:
            messages.error(request, f"TRANSMISSION FAILED: {e}")

    return render(request, 'legal/contact.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', intro, name='intro'),           # Root goes to intro.html
    path('home/', home, name='home'),        # /home/ goes to home.html
    path('blog/', include('blog.urls')),     # /blog/ routes to your lore
    path('marketplace/', include('marketplace.urls')),
    path('terms/', blog_views.legal_page, {'slug': 'terms'}, name='terms'),
    path('privacy/', blog_views.legal_page, {'slug': 'privacy'}, name='privacy'),
    path('contact/', contact, name='contact'),
    path('sitemap.xml', sitemap),
    path('robots.txt', lambda r: HttpResponse(open('/home/mehdimchow/mehdicafe/static/robots.txt').read(), content_type="text/plain")),
]