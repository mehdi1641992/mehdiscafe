from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, WebringSite

def bazaar(request):
    # Fetch active products and approved webring sites
    products = Product.objects.filter(is_active=True)
    webrings = WebringSite.objects.filter(approved=True)
    
    return render(request, 'marketplace/bazaar.html', {
        'products': products,
        'webrings': webrings
    })

def product_detail(request, pk):
    # Fetch a single product by its Primary Key (ID)
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'marketplace/product_detail.html', {'product': product})

def join_webring(request):
    # Handle the webring submission form
    if request.method == 'POST':
        site_name = request.POST.get('site_name')
        site_url = request.POST.get('site_url')
        description = request.POST.get('description')
        
        # Save to database (requires admin approval by default)
        WebringSite.objects.create(
            site_name=site_name,
            site_url=site_url,
            description=description,
            approved=False 
        )
        return redirect('join_success')
        
    return render(request, 'marketplace/join_webring.html')

def join_success(request):
    # Show the success message after submitting to the webring
    return render(request, 'marketplace/join_success.html')