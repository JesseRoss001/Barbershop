from django.shortcuts import render, redirect
from .models import Booking, Service, Staff, BusinessHours
from django.http import HttpResponse

# Client Views
def book_view(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'booking/book_view.html', context)

def submit_booking(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        staff_id = request.POST.get('staff')
        date_time = request.POST.get('date_time')
        client_name = request.POST.get('client_name')
        client_contact = request.POST.get('client_contact')

        service = Service.objects.get(id=service_id)
        staff = Staff.objects.get(id=staff_id)
        
        booking = Booking(
            client_name=client_name,
            client_contact=client_contact,
            service=service,
            staff=staff,
            date_time=date_time
        )
        booking.save()
        return HttpResponse("Booking successfully created!")
    return redirect('book_view')

# Admin Views
def admin_dashboard(request):
    bookings = Booking.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'bookings': bookings})
