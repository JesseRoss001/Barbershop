from django.contrib import admin
from .models import Service, Staff, BusinessHours, Booking, GalleryImage

class BusinessHoursInline(admin.TabularInline):
    model = BusinessHours
    extra = 1

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    inlines = [BusinessHoursInline]

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'staff', 'date_time', 'client_contact')
    list_filter = ('date_time', 'service', 'staff')
    search_fields = ['client_name', 'client_contact']

admin.site.register(Service)
admin.site.register(Staff, StaffAdmin)
admin.site.register(BusinessHours)
admin.site.register(Booking, BookingAdmin)
admin.site.register(GalleryImage)
