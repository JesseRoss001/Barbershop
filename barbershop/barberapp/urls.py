from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),  # New URL for the about page
    path('blog/', views.blog, name='blog'),     # New URL for the blog page
]
