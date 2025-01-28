from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (CustomTokenObtainView, CustomRefreshTokenView, is_authenticated,  home_view,
                    login_view, register_api, register, logout_redirect_view, profile, EditProfileView)

urlpatterns = [
    path('login/token/home/', home_view, name='home_view'),
    path('login/token/', CustomTokenObtainView.as_view(), name='login_token'),
    path('token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('home/logout/', logout_redirect_view, name='logout_view'),
    path('home/register/', register, name='register'),
    path('register_api/', register_api, name='register_api'),
    path('authenticated/', is_authenticated),
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_redirect_view, name='logout_view'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
