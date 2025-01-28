from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import logging
logger = logging.getLogger(__name__)

class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None
        logger.debug(f'Access token from cookies: {access_token}')
        validated_token = self.get_validated_token(access_token)

        try:
            user = self.get_user(validated_token)
        except AuthenticationFailed:
            logger.error("Token validation failed")
            return None

        return user, validated_token