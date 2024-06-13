from django.contrib import admin
from .models import Service, Staff, Booking, BusinessHours, GalleryImage

class BookingAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'service', 'staff', 'date_time', 'client_contact']
    list_filter = ['date_time', 'service', 'staff']

admin.site.register(Service)
admin.site.register(Staff)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BusinessHours)
admin.site.register(GalleryImage)
