from django.db import models
from django.contrib.auth.models import User
class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField(help_text="Duration of the service")
class WorkingHours(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ]
    
    day_of_week = models.IntegerField(choices=DAY_CHOICES, help_text="Day of the week")
    working = models.BooleanField(default=True, help_text="Is the staff member working on this day?")
    arriving_time = models.TimeField(blank=True, null=True, help_text="Arriving time")
    leaving_time = models.TimeField(blank=True, null=True, help_text="Leaving time")
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='working_hours')

    def __str__(self):
        status = "Working" if self.working else "Not Working"
        return f"{self.get_day_of_week_display()} - {status}"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, help_text="Phone number")

    def __str__(self):
        return self.name

class Booking(models.Model):
    client_name = models.CharField(max_length=100)
    client_contact = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
