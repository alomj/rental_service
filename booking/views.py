from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from booking.models import Booking, BookingStatus
from booking.serializer import BookingSerializer

User = get_user_model()


class BookingFilter(filters.FilterSet):
    min_created_at = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    max_created_at = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    hotel_name = filters.CharFilter(field_name='hotel__name', lookup_expr='icontains')


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'created_at', 'hotel', 'car', 'flight']
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        if not isinstance(user, User):
            raise ValueError("Invalid user instance in get_queryset.")
        return self.queryset.filter(created_by=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def validate_update(self, instance):
        if instance.status == BookingStatus.CANCELLED:
            raise ValidationError({"detail": "Cannot update a cancelled booking."})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        self.validate_update(instance)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != BookingStatus.ACTIVE:
            return Response(
                {'error': "Only active bookings can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.status = BookingStatus.CANCELLED
        instance.save()
        return Response({"detail": "Booking cancelled successfully."})
