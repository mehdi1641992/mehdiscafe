# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Your existing blog paths (yours might look a little different, leave them as they are!)
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]