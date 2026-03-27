from django.urls import path
from . import views

urlpatterns = [
    path('', views.bazaar, name='bazaar'),
    path('join-webring/', views.join_webring, name='join_webring'),
]