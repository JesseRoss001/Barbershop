from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.book_view, name='booking'),
    path('submit_booking/', views.submit_booking, name='submit_booking'),  # Ensure this line is added
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
]
