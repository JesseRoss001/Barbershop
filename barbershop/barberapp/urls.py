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
    path('login/', views.staff_login, name='login'),
    path('register/', views.staff_register, name='register'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='barberapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='barberapp/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
