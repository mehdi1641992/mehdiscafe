from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from blog.models import Post
from marketplace.models import Product
from blog import views as blog_views
import os

# --- 1. LOCAL VIEW FUNCTIONS (Defined right here) ---

def intro(request):
    return render(request, 'intro.html')

def home(request):
    latest_posts = Post.objects.all().order_by('-created_at')[:4]
    featured_products = Product.objects.filter(is_active=True)[:4]
    return render(request, 'home.html', {
        'posts': latest_posts,
        'products': featured_products
    })

def about(request):
    # This renders your standalone about page at templates/about.html
    return render(request, 'about.html')

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

    # Renders the contact page at templates/legal/contact.html
    return render(request, 'legal/contact.html')

def sitemap(request):
    posts = Post.objects.all()
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    pages = ['', '/home/', '/blog/', '/marketplace/', '/contact/', '/privacy/']
    for page in pages:
        xml_content += f'<url><loc>https://mehdimchow.pythonanywhere.com{page}</loc><changefreq>weekly</changefreq></url>'
    for post in posts:
        xml_content += f'<url><loc>https://mehdimchow.pythonanywhere.com/blog/{post.id}/</loc><lastmod>{post.created_at.strftime("%Y-%m-%d")}</lastmod></url>'
    xml_content += '</urlset>'
    return HttpResponse(xml_content, content_type="application/xml")


# --- 2. URL PATTERNS ---

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    
    # These point to the functions defined above
    path('', intro, name='intro'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),     # Corrected reference
    path('contact/', contact, name='contact'), # Corrected reference
    
    path('blog/', include('blog.urls')),
    path('marketplace/', include('marketplace.urls')),
    
    # These use the database logic from blog/views.py
    path('terms/', blog_views.legal_page, {'slug': 'terms'}, name='terms'),
    path('privacy/', blog_views.legal_page, {'slug': 'privacy'}, name='privacy'),
    
    path('sitemap.xml', sitemap),
    path('robots.txt', lambda r: HttpResponse(
        open('/home/mehdimchow/mehdicafe/static/robots.txt').read(), 
        content_type="text/plain"
    )),
]