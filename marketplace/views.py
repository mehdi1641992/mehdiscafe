from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, WebringSite

def bazaar(request):
    products = Product.objects.filter(is_active=True)
    webrings = WebringSite.objects.filter(approved=True)
    return render(request, 'marketplace/bazaar.html', {
        'products': products, 
        'webrings': webrings
    })

def join_webring(request):
    if request.method == 'POST':
        site_name = request.POST.get('site_name')
        site_url = request.POST.get('site_url')
        description = request.POST.get('description')
        email = request.POST.get('email')

        # Save the application as unapproved
        WebringSite.objects.create(
            site_name=site_name,
            site_url=site_url,
            description=f"{description} (Contact: {email})"
        )
        
        return render(request, 'marketplace/join_success.html')

    return render(request, 'marketplace/join_webring.html')