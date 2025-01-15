from django.contrib import admin
from .models import Booking, Hotel, Car, Flight

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'status', 'hotel', 'car', 'flight')
    search_fields = ('created_by__username', 'hotel__name','flight__flight_number')
    list_filter = ('status', 'hotel', 'car', 'flight')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'room_type')
    search_fields = ('name', 'location')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', )
    search_fields = ['model']


from django.contrib import admin
from .models import Flight


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'airline',
        'flight_number',
        'date_of_departure',
        'departure_time',
        'arrival_time',
        'place_of_departure',
        'destination',
        'price',
        'seat_class',
        'is_direct'
    )

    search_fields = ('airline', 'flight_number', 'place_of_departure', 'destination')

    list_filter = ('date_of_departure', 'is_direct', 'seat_class', 'place_of_departure', 'destination')

    fieldsets = (
        ('Main Information', {
            'fields': ('airline', 'flight_number', 'seat_class', 'is_direct')
        }),
        ('Час і місце', {
            'fields': ('date_of_departure', 'departure_time', 'arrival_time', 'place_of_departure', 'destination')
        }),
        ('Ціна та зображення', {
            'fields': ('price', 'image')
        }),
    )

    ordering = ('date_of_departure', 'departure_time')
