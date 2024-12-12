from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

class TokenRefreshMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = [
            '/login/',
            '/register/',
            '/register_api/',
            '/static/',
            '/api/register_api/',
            '/logout'
        ]

        if any(request.path.startswith(path) for path in excluded_paths):
            return None

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token and refresh_token:
            try:
                new_token = RefreshToken(refresh_token)
                new_access_token = str(new_token.access_token)

                request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                request.access_token_refreshed = True
            except AuthenticationFailed:
                return redirect('/login/')

        elif not access_token and not refresh_token:
            return redirect('/login/')

        return None

    def process_response(self, request, response):
        if getattr(request, 'access_token_refreshed', False):
            access_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
        return response