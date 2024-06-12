from django.urls import path ,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('gallery/', views.gallery, name='gallery'),
]


