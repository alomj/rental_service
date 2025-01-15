from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FlightView, TicketView, TicketPDFView, BuyTicketView, CarView, CarRent, BookingRenderList, \
    BookingViewSet, CarSuccessfulRent, HotelList, HotelRent, HotelSuccessfulRent
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    # API paths
    path('api/', include(router.urls)),

    # Ticket and Flight Views
    path('success/', TicketView.as_view(), name='success_ticket'),
    path('ticket/<slug:flight_slug>/<int:ticket_id>/', TicketView.as_view(), name='show_ticket'),
    path('ticket/success/<slug:flight_slug>/<int:ticket_id>', TicketView.as_view(), name='success_ticket'),
    path('ticket/<slug:flight_slug>/<int:ticket_id>/pdf/', TicketPDFView.as_view(), name='ticket_pdf'),

    # Booking Views
    path('bookings/', BookingRenderList.as_view(), name='booking'),
    path('flights/', FlightView.as_view(), name='flights'),
    path('ticket_buy/<slug:flight_slug>/', BuyTicketView.as_view(), name='ticket_buy'),

    # Car views
    path('cars/', CarView.as_view(), name='car_list'),
    path('car_rent/<slug:car_slug>/', CarRent.as_view(), name='car_rent'),
    path('cars/<int:car_id>/ticket', CarSuccessfulRent.as_view(), name='successfull'),
    path('hotels/', HotelList.as_view(), name='hotel_list'),
    path('hotels/<slug:hotel_slug>/', HotelRent.as_view(), name='hotel_book'),
    path('hotels/<slug:hotel_slug>/<int:hotel_id>/', HotelSuccessfulRent.as_view(), name='h_successful')




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
