from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField(help_text="Duration of the service")

    def __str__(self):
        return self.name

class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    working = models.BooleanField(default=False)
    arriving_time = models.TimeField(null=True, blank=True)
    leaving_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

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

    def __str__(self):
        return f"Booking for {self.client_name} with {self.staff.name} on {self.date_time}"

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or "Gallery Image"
