from requests import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking
from booking.serializer import BookingSerializer


class CreateBookingView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Booking created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )