# Ejemplo: Custom Claims + Blacklist/Revocación con SimpleJWT


# -------------------------------------------------#
# 1. Serializer con Custom Claims
# -------------------------------------------------#
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Inyecta claims adicionales en el access token.

    NOTA: super().get_token(user) ya incluye los claims por defecto de SimpleJWT:
      - token_type  ("access")
      - exp          (expiración)
      - iat          (issued at)
      - jti          (JWT ID único)
      - user_id      (PK del usuario)

    Los claims que se agregan aquí se SUMAN a los anteriores,
    no los reemplazan.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Claims custom (se agregan a los ya existentes)
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['role'] = getattr(user, 'role', 'user')

        return token


# -------------------------------------------------#
# 2. Vista de Login con claims custom
# -------------------------------------------------#
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# -------------------------------------------------#
# 3. Vista de Logout (blacklist manual)
# -------------------------------------------------#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class LogoutView(APIView):
    """
    Recibe el refresh token y lo blacklistea.
    Sin refresh token válido el usuario no puede renovar el access.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except (KeyError, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------#
# 4. URLs
# -------------------------------------------------#
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
"""


# -------------------------------------------------#
# 5. Settings relevantes
# -------------------------------------------------#
"""
# src/core/settings.py

INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt.token_blacklist',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_OBTAIN_SERIALIZER': 'users.serializers.CustomTokenObtainPairSerializer',
}
"""
