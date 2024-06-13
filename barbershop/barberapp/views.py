from django.shortcuts import render

def home(request):
    return render(request, 'barberapp/home.html')

def booking(request):
    services = Service.objects.all()
    return render(request, 'barberapp/booking.html', {'services': services})

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'barberapp/gallery.html', {'images': images})

def about(request):
    return render(request, 'barberapp/about.html')  # Render an about page template

def blog(request):
    return render(request, 'barberapp/blog.html')  # Render a blog page template
