from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()

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
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(default='00:00')  # Add a default value
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(default='default@example.com')
    customer_phone = models.CharField(max_length=15, default='+440000000000')
    staff = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service.name} for {self.customer_name} on {self.date} at {self.time} with {self.staff.username}"

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or "Gallery Image"
