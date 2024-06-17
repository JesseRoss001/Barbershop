from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Staff, Availability, Booking, GalleryImage

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'working', 'arriving_time', 'leaving_time')
    list_filter = ('user', 'working')
    search_fields = ('user__username', 'date')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'staff', 'date_time', 'client_contact')
    list_filter = ('date_time', 'service', 'staff')
    search_fields = ['client_name', 'client_contact']

admin.site.register(Service)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Availability, AvailabilityAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(GalleryImage)
