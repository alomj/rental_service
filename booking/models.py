from django.db import models
from django.db.models import ForeignKey

from user.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date_of_arrival = models.DateField()
    departure_date = models.DateField()
    room_type = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_guests = models.IntegerField()
    is_breakfast_included = models.BooleanField(default=False)
    special_requests = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='hotels/', blank=True, null=False, default='images/default-hotel.jpg')

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_insurance_included = models.BooleanField(default=False)
    mileage_limit = models.IntegerField(null=True, blank=True)
    special_requirements = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=False, default='images/default-car.jpg')


class Flight(models.Model):
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=50)
    date_of_departure = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    place_of_departure = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_class = models.CharField(max_length=50)
    is_direct = models.BooleanField(default=True)
    image = models.ImageField(upload_to='flights/', blank=True, null=False, default='images/default-flight.jpg')

class Ticket(models.Model):
    flight = ForeignKey(Flight, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=255)
    email = models.EmailField()
    purchase_data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Ticket for {self.passenger_name} on {self.flight}'



class BookingStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    CANCELLED = 'CANCELLED', 'Cancelled'
    COMPLETED = 'COMPLETED', 'Completed'

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(
        max_length=10,
        choices=BookingStatus.choices,
        default=BookingStatus.ACTIVE,
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
