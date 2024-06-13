from django.shortcuts import render, redirect, HttpResponse
from .models import Booking, Service, Staff, BusinessHours, GalleryImage
from django.utils import timezone
import datetime

def home(request):
    return render(request, 'barberapp/home.html')

def book_view(request):
    today = datetime.date.today()
    next_30_days = [today + datetime.timedelta(days=i) for i in range(30)]
    services = Service.objects.all()
    available_times = {day: [] for day in next_30_days}
    
    for day in next_30_days:
        for hour in range(9, 17):  # assuming business hours from 9 to 17
            available_times[day].append(f"{hour}:00")
    
    context = {
        'services': services,
        'days': next_30_days,
        'available_times': available_times
    }
    return render(request, 'barberapp/book_view.html', context)

def submit_booking(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        date_time = request.POST.get('date_time')
        client_name = request.POST.get('client_name')
        client_contact = request.POST.get('client_contact')
        staff = Staff.objects.first()  # simplification; should choose based on availability

        service = Service.objects.get(id=service_id)
        booking = Booking(client_name=client_name, client_contact=client_contact, service=service, staff=staff, date_time=date_time)
        booking.save()
        return HttpResponse("Booking successfully created!")
    return redirect('book_view')

def admin_dashboard(request):
    bookings = Booking.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    return render(request, 'barberapp/admin_dashboard.html', {'bookings': bookings})

def about(request):
    return render(request, 'barberapp/about.html')

def blog(request):
    return render(request, 'barberapp/blog.html')

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'barberapp/gallery.html', {'images': images})
