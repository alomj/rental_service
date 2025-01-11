from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FlightView, TicketView, TicketPDFView, BuyTicketView, CarView, CarRent, BookingRenderList, \
    BookingViewSet, CarSuccesfullRent
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    # API paths
    path('api/', include(router.urls)),

    # Ticket and Flight Views
    path('success/', TicketView.as_view(), name='success_ticket'),
    path('ticket/show/<int:ticket_id>/', TicketView.as_view(), name='show_ticket'),
    path('ticket/success/<int:ticket_id>/', TicketView.as_view(), name='success_ticket'),
    path('ticket/pdf/<int:ticket_id>/', TicketPDFView.as_view(), name='ticket_pdf'),

    # Booking Views
    path('bookings/', BookingRenderList.as_view(), name='booking'),
    path('flights/', FlightView.as_view(), name='flights'),
    path('ticket_buy/<int:flight_id>/', BuyTicketView.as_view(), name='ticket_buy'),

    # Car views
    path('cars/', CarView.as_view(), name='car_list'),
    path('car_rent/<int:car_id>/', CarRent.as_view(), name='car_rent'),
    path('cars/<int:car_id>/ticket', CarSuccesfullRent.as_view(), name='successfull')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
