from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Staff, BusinessHours, Booking, GalleryImage



class BusinessHoursInline(admin.TabularInline):
    model = BusinessHours
    fields = ['day_of_week', 'is_open', 'open_time', 'close_time', 'lunch_start', 'lunch_end']
    template = 'admin/barberapp/BusinessHours/inline.html'  # Correct path to your new custom template
    extra = 0  # No extra forms by default
    min_num = 7  # Ensures a week's schedule is set
    max_num = 7  # Limits to exactly seven days

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'weekly_hours_display')

    inlines = [BusinessHoursInline]

    def weekly_hours_display(self, obj):
        hours = BusinessHours.objects.filter(staff=obj)
        display_html = ""
        for hour in hours:
            display_html += f"<div><strong>{hour.get_day_of_week_display()}:</strong> "
            if hour.is_open:
                display_html += f"{hour.open_time.strftime('%H:%M')} - {hour.close_time.strftime('%H:%M')} "
                display_html += f"(Lunch: {hour.lunch_start.strftime('%H:%M')} - {hour.lunch_end.strftime('%H:%M')})"
            else:
                display_html += "Closed"
            display_html += "</div>"
        return format_html(display_html)

    weekly_hours_display.short_description = "Weekly Hours"



class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'staff', 'date_time', 'client_contact')
    list_filter = ('date_time', 'service', 'staff')
    search_fields = ['client_name', 'client_contact']

admin.site.register(Service)
admin.site.register(Staff, StaffAdmin)
admin.site.register(BusinessHours)
admin.site.register(Booking, BookingAdmin)
admin.site.register(GalleryImage)
