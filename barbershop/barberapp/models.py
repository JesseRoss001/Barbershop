from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField(help_text="Duration of the service")

class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class BusinessHours(models.Model):
    day_of_week = models.IntegerField(help_text="0 = Monday, 6 = Sunday")
    open_time = models.TimeField()
    close_time = models.TimeField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

class Booking(models.Model):
    client_name = models.CharField(max_length=100)
    client_contact = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
