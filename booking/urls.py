from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, BookingRenderList, success_ticket, flight_list, ticket_buy, show_ticket
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    # Шляхи API
    path('success/', success_ticket, name='success_ticket'),
    path('api/', include(router.urls)),

    path('bookings/', BookingRenderList.as_view(), name='booking'),
    path('flights/', flight_list, name = 'flights'),
    path('ticket_buy/<int:flight_id>/', ticket_buy, name='ticket_buy'),
    path('ticket/show/<int:ticket_id>/', show_ticket, name='show_ticket'),
    path('ticket/success/<int:ticket_id>/', success_ticket, name='success_ticket'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
