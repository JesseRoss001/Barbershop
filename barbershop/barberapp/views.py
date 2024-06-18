import logging
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from .forms import CustomUserCreationForm  # Import the custom form
from .models import Booking, Service, Staff, Availability, GalleryImage
from django.utils import timezone
from datetime import timedelta, datetime
from .utils import send_email, send_sms 

from django.views.decorators.csrf import csrf_exempt
import re


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
        user = request.user
        data = request.POST

        try:
            logger.debug("Received POST data: %s", data)

            for key, value in data.items():
                if key.endswith('_working'):
                    date_str = key.replace('_working', '')
                    logger.debug("Processing date: %s", date_str)
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    working = value == 'on'
                    arriving_time_str = data.get(f'{date_str}_arriving_time', '')
                    leaving_time_str = data.get(f'{date_str}_leaving_time', '')

                    arriving_time = None
                    leaving_time = None

                    if working:
                        if arriving_time_str:
                            arriving_time = datetime.strptime(arriving_time_str, '%H:%M').time()
                        if leaving_time_str:
                            leaving_time = datetime.strptime(leaving_time_str, '%H:%M').time()
                        if arriving_time is None or leaving_time is None:
                            return JsonResponse({'status': 'error', 'message': 'Arriving and leaving times must be set if working is checked.'}, status=400)

                    Availability.objects.update_or_create(
                        user=user,
                        date=date,
                        defaults={
                            'working': working,
                            'arriving_time': arriving_time,
                            'leaving_time': leaving_time
                        }
                    )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error("Error saving availability: %s", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    days = [timezone.now().date() + timedelta(days=i) for i in range(60)]
    availability = {day: Availability.objects.filter(user=request.user, date=day).first() for day in days}

    return render(request, 'barberapp/availability.html', {'days': days, 'availability': availability})
def book_view(request):
    services = [
        {'name': 'Haircut', 'duration': timedelta(minutes=30)},
        {'name': 'Beard', 'duration': timedelta(minutes=15)},
        {'name': 'Dying Hair', 'duration': timedelta(hours=2, minutes=30)},
        {'name': 'Combo Hair and Beard', 'duration': timedelta(minutes=40)}
    ]
    for service_data in services:
        Service.objects.update_or_create(name=service_data['name'], defaults={'duration': service_data['duration']})

    services = Service.objects.all()
    return render(request, 'barberapp/book_appointment.html', {'services': services})
def get_available_dates(request):
    service_id = request.GET.get('service_id')
    if not service_id:
        return JsonResponse({'dates': [], 'heatmap': {}})

    service = Service.objects.get(id=service_id)
    service_duration = service.duration  # Duration of the selected service

    available_dates = Availability.objects.filter(working=True).values_list('date', flat=True).distinct()
    available_dates_list = list(available_dates)

    # Heatmap colors logic
    date_heatmap = {}
    for date in available_dates_list:
        slots = Availability.objects.filter(date=date, working=True).count()
        if slots >= 5:
            color = 'green'
        elif 3 <= slots < 5:
            color = 'yellow'
        else:
            color = 'red'
        date_heatmap[str(date)] = color

    return JsonResponse({'dates': available_dates_list, 'heatmap': date_heatmap})
@csrf_exempt
def submit_booking(request):
    if request.method == 'POST':
        logger.debug("Received POST data: %s", request.POST)

        service_id = request.POST.get('service')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        client_name = request.POST.get('customer_name')
        client_email = request.POST.get('customer_email')
        client_phone = request.POST.get('customer_phone')
        staff_id = request.POST.get('staff')

        logger.debug("Service ID: %s, Date: %s, Time: %s, Customer Name: %s, Customer Email: %s, Customer Phone: %s, Staff ID: %s",
                     service_id, date_str, time_str, client_name, client_email, client_phone, staff_id)

        if not all([service_id, date_str, time_str, client_name, client_email, client_phone, staff_id]):
            messages.error(request, 'All fields are required.')
            logger.error('Form submission aborted. Missing required fields.')
            return redirect('book_view')

        try:
            # Validate email and phone number
            email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            phone_regex = re.compile(r'^(?:\+44|0044|0)?[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}$')

            if not email_regex.match(client_email):
                messages.error(request, 'Invalid email format.')
                logger.error('Invalid email format: %s', client_email)
                return redirect('book_view')

            if not phone_regex.match(client_phone):
                messages.error(request, 'Invalid phone number format. It must be a valid UK phone number.')
                logger.error('Invalid phone number format: %s', client_phone)
                return redirect('book_view')

            service = Service.objects.get(id=service_id)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()
            staff = Staff.objects.get(user__id=staff_id)

            start_time = datetime.combine(date, time)
            end_time = start_time + service.duration

            # Check for overlapping bookings
            overlapping_booking = Booking.objects.filter(
                date=date,
                staff=staff.user,
                time__lt=end_time.time(),
                end_time__gt=start_time.time()
            ).exists()

            if overlapping_booking:
                messages.error(request, 'This time slot is already booked.')
                logger.error('Double booking attempt: Service: %s, Date: %s, Time: %s, Staff: %s',
                             service.name, date, time, staff.name)
                return redirect('book_view')

            Booking.objects.create(
                service=service,
                date=date,
                time=time,
                end_time=end_time.time(),
                customer_name=client_name,
                customer_email=client_email,
                customer_phone=client_phone,
                staff=staff.user
            )

            # Send Email
            email_content = f"Dear {client_name},\nYour booking for {service.name} on {date_str} at {time_str} is confirmed."
            send_email(client_email, "Booking Confirmation", email_content)

            # Send SMS
            sms_content = f"Dear {client_name}, your booking for {service.name} on {date_str} at {time_str} is confirmed."
            send_sms(client_phone, sms_content)

            messages.success(request, 'Your appointment has been booked successfully.')
            logger.info('Booking created successfully: Service: %s, Date: %s, Time: %s, Customer: %s, Staff: %s',
                        service.name, date, time, client_name, staff.name)
            return redirect('booking_success')
        except Service.DoesNotExist:
            logger.error('Service with ID %s does not exist.', service_id)
            messages.error(request, 'Selected service does not exist.')
        except Staff.DoesNotExist:
            logger.error('Staff with ID %s does not exist.', staff_id)
            messages.error(request, 'Selected staff does not exist.')
        except Exception as e:
            logger.error("Error during booking submission: %s", e)
            messages.error(request, 'An error occurred during booking. Please try again.')

        return redirect('book_view')

    services = Service.objects.all()
    return render(request, 'barberapp/book_appointment.html', {'services': services})
def get_available_times(request):
    service_id = request.GET.get('service_id')
    date_str = request.GET.get('date')

    if not service_id or not date_str:
        return JsonResponse({'times': []})

    service = Service.objects.get(id=service_id)
    service_duration = service.duration  # Duration of the selected service
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    available_times = {}
    staff_availability = Availability.objects.filter(date=date, working=True)
    for availability in staff_availability:
        start_time = datetime.combine(date, availability.arriving_time)
        end_time = datetime.combine(date, availability.leaving_time)

        while start_time + service_duration <= end_time:
            end_slot_time = start_time + service_duration

            # Check if the time slot is already booked
            overlapping_booking = Booking.objects.filter(
                date=date,
                staff=availability.user,
                time__lt=end_slot_time.time(),
                end_time__gt=start_time.time()
            ).exists()

            if not overlapping_booking:
                date_str = date.strftime('%Y-%m-%d')
                if date_str not in available_times:
                    available_times[date_str] = []
                available_times[date_str].append({
                    'time': start_time.time().strftime('%H:%M'),
                    'staff': availability.user.username,
                    'staff_id': availability.user.id
                })

            start_time += timedelta(minutes=5)  # Check every 5 minutes to find fitting slots

    return JsonResponse({'available_times': available_times})

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

def custom_logout_view(request):
    logout(request)
    return redirect('home')
