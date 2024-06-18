from django.contrib import admin
from .models import Service, Staff, Availability, Booking, GalleryImage

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'working', 'arriving_time', 'leaving_time')
    list_filter = ('user', 'working')
    search_fields = ('user__username', 'date')
    ordering = ('date',)  # Ensure dates are displayed in order

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'date', 'time', 'customer_contact', 'staff')
    list_filter = ('date', 'staff', 'service')

admin.site.register(Service)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Availability, AvailabilityAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(GalleryImage)
