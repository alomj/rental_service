from rest_framework import serializers

from user.models import User
from .models import Hotel, Flight, Car, Booking


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'date_of_arrival', 'departure_date', 'room_type']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'rental_start_date', 'rental_end_date']


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['airline', 'flight_number', 'date_of_departure', 'departure_time']


class BookingSerializer(serializers.ModelSerializer):
    hotel_details = HotelSerializer(source='hotel', read_only=True)
    car_details = CarSerializer(source='car', read_only=True)
    flight_details = FlightSerializer(source='flight', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'created_at', 'created_by', 'status',
            'hotel', 'car', 'flight',
            'hotel_details', 'car_details', 'flight_details'
        ]
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create a booking.")

        if not isinstance(request.user, User):
            raise serializers.ValidationError("Invalid user instance.")

        validated_data['created_by'] = request.user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not instance.hotel:
            representation.pop('hotel_details', None)
        if not instance.car:
            representation.pop('car_details', None)
        if not instance.flight:
            representation.pop('flight_details', None)

        if instance.status == 'CANCELLED':
            representation['status_message'] = 'This booking has been cancelled.'

        return representation
