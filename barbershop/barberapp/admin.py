from django.contrib import admin
from .models import Service, Staff, BusinessHours, Booking, GalleryImage

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('staff', 'day_of_week', 'open_time', 'close_time')
    list_filter = ('day_of_week', 'staff')
    ordering = ('day_of_week',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'staff', 'date_time', 'client_contact')
    list_filter = ('date_time', 'service', 'staff')
    search_fields = ['client_name', 'client_contact']

admin.site.register(Service)
admin.site.register(Staff, StaffAdmin)
admin.site.register(BusinessHours, BusinessHoursAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(GalleryImage)
