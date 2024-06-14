from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField(help_text="Duration of the service")

class BusinessHours(models.Model):
    DAY_CHOICES = [(i, day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])]
    
    day_of_week = models.IntegerField(choices=DAY_CHOICES, help_text="Day of the week")
    is_open = models.BooleanField(default=True, help_text="Is the business open on this day?")
    open_time = models.TimeField(blank=True, null=True, help_text="Opening time")
    close_time = models.TimeField(blank=True, null=True, help_text="Closing time")
    lunch_start = models.TimeField(blank=True, null=True, help_text="Start of lunch break")
    lunch_end = models.TimeField(blank=True, null=True, help_text="End of lunch break")
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='business_hours')

    def __str__(self):
        status = "Open" if self.is_open else "Closed"
        return f"{self.get_day_of_week_display()} - {status}"

class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

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
