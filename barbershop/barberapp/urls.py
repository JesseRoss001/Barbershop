from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_view, name='book_view'),
    path('book/submit/', views.submit_booking, name='submit_booking'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('gallery/', views.gallery, name='gallery'),
    path('staff/availability/', views.staff_availability, name='staff_availability'),
]
