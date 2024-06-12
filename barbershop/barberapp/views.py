from django.shortcuts import render
from .models import Service, Booking, GalleryImage

def home(request):
    return render(request, 'home.html')

def booking(request):
    services = Service.objects.all()
    return render(request, 'booking.html', {'services': services})

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})

