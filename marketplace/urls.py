from django.urls import path
from . import views

urlpatterns = [
    path('', views.bazaar, name='bazaar'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # Add this
    path('join-webring/', views.join_webring, name='join_webring'),
    path('join-success/', views.join_success, name='join_success'),
]