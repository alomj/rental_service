import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from weasyprint import HTML

from .forms import BuyTicketForm, CarRentalForm, HotelRentalForm
from .models import Flight, Ticket, Car, Hotel


class FlightView(LoginRequiredMixin, View):
    def get(self, request):
        flights = Flight.objects.all().order_by('flight_number')
        query = request.GET.get('q', ' ')

        if query:
            flights = flights.filter(
                Q(flight_number__icontains=query) | Q(destination__icontains=query) | Q(airline__icontains=query)
            )

        paginator = Paginator(flights, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'booking/flight/flight_list.html', {'flights': page_obj,
                                                                   'query': query})


class TicketView(View):
    def get(self, request, flight_slug, ticket_id):
        ticket = get_object_or_404(Ticket, flight__slug=flight_slug, id=ticket_id)
        return render(request, 'booking/flight/success_ticket.html', {'ticket': ticket,
                                                                      'flight': ticket.flight})


class TicketPDFView(View):
    def get(self, request, flight_slug, ticket_id):
        ticket = get_object_or_404(Ticket, flight__slug=flight_slug, id=ticket_id)
        html_content = render_to_string('booking/flight/ticket_template.html', {'ticket': ticket})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.flight.slug}_{ticket.id}.pdf"'

        HTML(string=html_content).write_pdf(response)
        return response


class BuyTicketView(View):
    def get(self, request, flight_slug):
        flight = get_object_or_404(Flight, slug=flight_slug)
        form = BuyTicketForm()
        return render(request, 'booking/flight/buy_ticket.html', {'flight': flight, 'form': form})

    def post(self, request, flight_slug):
        flight = get_object_or_404(Flight, slug=flight_slug)
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.flight = flight
            ticket.save()
            return redirect('show_ticket', flight_slug=flight.slug, ticket_id=ticket.id)
        return render(request, 'booking/flight/buy_ticket.html', {'flight': flight, 'form': form})


class CarView(LoginRequiredMixin, View):
    def get(self, request):
        cars = Car.objects.all().order_by('model')
        query = request.GET.get('q', ' ')
        if query:
            cars = cars.filter(Q(model__icontains=query) & Q(year__icontains=query) | Q(model__icontains=query) &
                               Q(class_of_car__icontains=query) | Q(model__icontains=query))

        paginator = Paginator(cars, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'booking/car/car_list.html', {'cars': page_obj, 'query': query})


class CarRent(LoginRequiredMixin, View):
    def get(self, request, car_slug):
        car = get_object_or_404(Car, slug=car_slug)
        form = CarRentalForm(car=car)
        return render(request, 'booking/car/car_rent.html', {'car': car, 'form': form})

    def post(self, request, car_slug):
        car = get_object_or_404(Car, slug=car_slug)
        form = CarRentalForm(request.POST, car=car)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.user = request.user
            rental_start_date = form.cleaned_data['rental_start_date']
            rental_end_date = form.cleaned_data['rental_end_date']
            total_price = form.cleaned_data['total_price']

            rental.save()
            request.session['rental_start_date'] = str(rental_start_date)
            request.session['rental_end_date'] = str(rental_end_date)
            request.session['total_price'] = str(total_price)

            return render(request, 'booking/car/car_succesful.html', {
                'car': car,
                'rental_start_date': rental_start_date,
                'rental_end_date': rental_end_date,
                'total_price': total_price
            })
        return render(request, 'booking/car/car_rent.html', {'car': car, 'form': form})


class CarSuccessfulRent(LoginRequiredMixin, View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)

        rental_start_date = request.session.get('rental_start_date')
        rental_end_date = request.session.get('rental_end_date')
        total_price = request.session.get('total_price')

        return render(request, 'booking/car/car_ticket.html', {
            'car_id': car_id,
            'car': car,
            'rental_start_date': rental_start_date,
            'rental_end_date': rental_end_date,
            'total_price': total_price
        })


class HotelList(LoginRequiredMixin, View):
    def get(self, request):
        hotel = Hotel.objects.all()

        query = request.GET.get('q', ' ')
        if query:
            hotel = hotel.filter(
                Q(name__icontains=query) | Q(location__icontains=query) |
                Q(name__icontains=query) & Q(location__icontains=query)
            )

        paginator = Paginator(hotel, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'booking/hotel/hotel_list.html', {'hotel': page_obj, 'query': query})

class HotelRent(LoginRequiredMixin, View):
    def get(self, request, hotel_slug):
        hotel = get_object_or_404(Hotel, slug=hotel_slug)
        form = HotelRentalForm(hotel=hotel)
        return render(request, 'booking/hotel/hotel_rent.html', {'hotel': hotel, 'form': form})

    def post(self, request, hotel_slug):
        hotel = get_object_or_404(Hotel, slug=hotel_slug)
        form = HotelRentalForm(request.POST, hotel=hotel)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.hotel = hotel
            rental.user = request.user
            arrival_date = form.cleaned_data['arrival_date']
            departure_date = form.cleaned_data['departure_date']
            total_price = form.cleaned_data['total_price']

            rental.save()
            request.session['arrival_date'] = str(arrival_date)
            request.session['departure_date'] = str(departure_date)
            request.session['total_price'] = str(total_price)

            return render(request, 'booking/hotel/hotel_succesful.html', {
                'hotel': hotel,
                'arrival_date': arrival_date,
                'departure_date': departure_date,
                'total_price': total_price
            })
        return render(request, 'booking/hotel/hotel_rent.html', {'hotel': hotel, 'form': form})


class HotelSuccessfulRent(LoginRequiredMixin, View):
    def get(self, request, hotel_slug, hotel_id):
        hotel = get_object_or_404(Hotel,slug=hotel_slug, id=hotel_id)

        arrival_date = request.session.get('arrival_date')
        departure_date = request.session.get('departure_date')
        total_price = request.session.get('total_price')

        return render(request, 'booking/hotel/hotel_ticket.html', {
            'hotel_id': hotel_id,
            'hotel': hotel,
            'arrival_date': arrival_date,
            'departure_date': departure_date,
            'total_price': total_price
        })


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
                context['bookings'] = []
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            context['bookings'] = []

        return context


from django.contrib.auth import get_user_model
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
