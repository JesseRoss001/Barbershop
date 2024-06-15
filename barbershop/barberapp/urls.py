from django.urls import path
from django.contrib.auth import views as auth_views  # Add this import
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
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='barberapp/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
