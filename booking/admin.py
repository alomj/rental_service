from django.contrib import admin
from .models import Booking, Hotel, Car, Flight

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'status', 'hotel', 'car', 'flight')
    search_fields = ('created_by__username', 'hotel__name', 'car__make', 'flight__flight_number')
    list_filter = ('status', 'hotel', 'car', 'flight')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'date_of_arrival', 'departure_date', 'room_type')
    search_fields = ('name', 'location')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'rental_start_date', 'rental_end_date')
    search_fields = ('make', 'model')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('airline', 'flight_number', 'date_of_departure', 'departure_time')
    search_fields = ('airline', 'flight_number')