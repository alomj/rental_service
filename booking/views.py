from django.shortcuts import render
from rest_framework import generics

from booking.models import Booking
from booking.serializer import BookingSerializer


class CreateBookingView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
