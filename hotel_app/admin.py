from django.contrib import admin, messages

# Register your models here.
from hotel_app.models import *

# admin acc
from django.contrib.auth.admin import UserAdmin
admin.site.register(Hotel)

 
class BookAdmin(admin.ModelAdmin):
    list_display = ("booking_num", "guest_ID", "checkin_date","checkout_date", "number_of_days", "check_out", "charge")
    list_filter = ["check_out", "no_of_guests","room_ID"]
    #search_fields = ["guest_ID"]

    def check_out(modeladmin, request, queryset):
        queryset.update(check_out=True)
        messages.success(request, "Selected Record(s) Marked as checkout Successfully !!")

    def check_in(modeladmin, request, queryset):
        queryset.update(check_out=False)
        messages.success(request, "Selected Record(s) Marked as checkin Successfully !!")


    admin.site.add_action(check_out, "Make Check out")
    admin.site.add_action(check_in, "Make Check in")


class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_no", "room_type", "no_of_beds","rate", "is_available")


class GuestAdmin(admin.ModelAdmin):
    list_display = ("email","phone","last_name","is_active", "date_joined")

class RatingAdmin(admin.ModelAdmin):
    list_display = ("created_at","rating","comment","guest_ID")
    list_filter = ["rating"]

class RatingAdmin(admin.ModelAdmin):
    list_display = ("created_at","rating","comment","guest_ID")
    list_filter = ["rating"]
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking_num","card_owner",)
    

admin.site.register(Guest,GuestAdmin)
admin.site.register(Booking, BookAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Payment, PaymentAdmin)


class CustomUserAdmin(UserAdmin):
    model = Guest
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)