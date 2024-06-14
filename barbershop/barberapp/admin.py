from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Staff, WorkingHours, Booking, GalleryImage

class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    fields = ['day_of_week', 'working', 'arriving_time', 'leaving_time']
    extra = 0
    min_num = 7
    max_num = 7

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'weekly_hours_display')
    inlines = [WorkingHoursInline]

    def weekly_hours_display(self, obj):
        hours = WorkingHours.objects.filter(staff=obj)
        display_html = ""
        for hour in hours:
            display_html += f"<div><strong>{hour.get_day_of_week_display()}:</strong> "
            if hour.working:
                display_html += f"{hour.arriving_time.strftime('%H:%M')} - {hour.leaving_time.strftime('%H:%M')}"
            else:
                display_html += "Not Working"
            display_html += "</div>"
        return format_html(display_html)

    weekly_hours_display.short_description = "Weekly Hours"

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'staff', 'date_time', 'client_contact')
    list_filter = ('date_time', 'service', 'staff')
    search_fields = ['client_name', 'client_contact']

admin.site.register(Service)
admin.site.register(Staff, StaffAdmin)
admin.site.register(WorkingHours)
admin.site.register(Booking, BookingAdmin)
admin.site.register(GalleryImage)
