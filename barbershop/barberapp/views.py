from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm  # Import the custom form
from .models import Booking, Service, Staff, WorkingHours, GalleryImage
from django.contrib.auth import views as auth_views
from django.utils import timezone
import logging
import datetime


# Setting up logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'barberapp/home.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if request.POST.get('registration_key') == 'Applejuice001@':
                user = form.save()
                Staff.objects.create(
                    user=user, 
                    name=user.username, 
                    email=form.cleaned_data.get('email'),
                    phone_number=form.cleaned_data.get('phone_number')
                )
                login(request, user)
                messages.success(request, 'Registration successful. Welcome!')
                return redirect('home')
            else:
                form.add_error('password2', 'Invalid registration key')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'barberapp/register.html', {'form': form})
def staff_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'barberapp/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'barberapp/login.html')


def staff_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        registration_key = request.POST.get('registration_key')
        if form.is_valid() and registration_key == 'Applejuice001@':
            user = form.save()
            Staff.objects.create(user=user, name=user.username, email=user.email)
            login(request, user)
            return redirect('home')
        else:
            form.add_error('password2', 'Invalid registration key or form is invalid')
    else:
        form = CustomUserCreationForm()
    return render(request, 'barberapp/register.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'barberapp/password_reset.html'
    email_template_name = 'barberapp/password_reset_email.html'
    subject_template_name = 'barberapp/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'barberapp/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


logger = logging.getLogger(__name__)

@login_required
def staff_availability(request):
    if request.method == 'POST':
        try:
            date_str = request.POST.get('date')
            working = request.POST.get('working') == 'true'
            arriving_time = request.POST.get('arriving_time')
            leaving_time = request.POST.get('leaving_time')

            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            day_of_week = date.weekday()

            WorkingHours.objects.update_or_create(
                staff=request.user.staff,
                day_of_week=day_of_week,
                defaults={
                    'working': working,
                    'arriving_time': arriving_time,
                    'leaving_time': leaving_time,
                }
            )
            logger.info("Availability updated for user %s on date %s", request.user.username, date_str)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error("Failed to update availability for user %s on date %s: %s", request.user.username, request.POST.get('date'), str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        today = datetime.date.today()
        days = [today + datetime.timedelta(days=i) for i in range(60)]
        context = {
            'days': days,
        }
        return render(request, 'barberapp/staff_availability.html', context)





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

def staff_availability(request):
    today = datetime.date.today()
    next_60_days = [today + datetime.timedelta(days=i) for i in range(60)]
    
    if request.method == 'POST':
        for day in next_60_days:
            working = request.POST.get(f'{day}_working', False)
            arriving_time = request.POST.get(f'{day}_arriving_time', None)
            leaving_time = request.POST.get(f'{day}_leaving_time', None)
                
            WorkingHours.objects.update_or_create(
                staff=request.user.staff,
                day_of_week=day.weekday(),
                defaults={
                    'working': working,
                    'arriving_time': arriving_time,
                    'leaving_time': leaving_time,
                }
            )
        return redirect('staff_availability')
    
    context = {
        'days': next_60_days,
    }
    return render(request, 'barberapp/staff_availability.html', context)


def custom_logout_view(request):
    logout(request)
    return redirect('home')
