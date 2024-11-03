from dj_rest_auth.views import LoginView
from rental_service.urls import path
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
