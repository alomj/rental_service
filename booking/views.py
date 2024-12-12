import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from .forms import BuyTicketForm
from .models import Flight, Ticket


@login_required
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'booking/flight/flight_list.html', {'flights': flights})

def show_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'booking/flight/success_ticket.html', {'ticket': ticket})



def success_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    html_content = render_to_string('booking/flight/ticket_template.html', {'ticket': ticket})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'

    HTML(string=html_content).write_pdf(response)
    return response


def ticket_buy(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == "POST":
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.flight = flight
            ticket.save()
            return redirect('show_ticket', ticket_id=ticket.id)
    else:
        form = BuyTicketForm()
    return render(request, 'booking/flight/buy_ticket.html', {'flight': flight, 'form': form})


class BookingRenderList(TemplateView):
    template_name = "booking/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            response = requests.get("http://localhost:8000/api/bookings/")
            if response.status_code == 200:
                context['bookings'] = response.json()
            else:
                print(f"Несподіваний статус відповіді: {response.status_code}")
                context['bookings'] = []  # Якщо статус не 200
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            context['bookings'] = []

        return context


from django.contrib.auth import get_user_model, login
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from booking.models import Booking, BookingStatus
from booking.serializer import BookingSerializer

User = get_user_model()


class BookingFilter(filters.FilterSet):
    min_created_at = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    max_created_at = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    hotel_name = filters.CharFilter(field_name='hotel__name', lookup_expr='icontains')


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'created_at', 'hotel', 'car', 'flight']

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
