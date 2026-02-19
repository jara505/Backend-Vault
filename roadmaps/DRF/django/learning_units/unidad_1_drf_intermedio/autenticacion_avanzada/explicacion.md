# Custom Claims y Blacklist/Revocación de Tokens (SimpleJWT)

## 1. Custom Claims

Los claims son los datos que viajan dentro del payload del JWT. Por defecto SimpleJWT incluye `user_id`, `token_type` y `exp`. Podés agregar los que necesites sobreescribiendo el serializer del token.

### Configuración en settings.py

```python
# src/core/settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    # Apuntar al serializer custom para inyectar claims
    'TOKEN_OBTAIN_SERIALIZER': 'users.serializers.CustomTokenObtainPairSerializer',
}
```

### Serializer con claims personalizados

```python
# users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Agrega claims al access token.
    Todo lo que pongas en token[] viaja en el payload del JWT.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Claims custom
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['role'] = getattr(user, 'role', 'user')

        return token
```

### Vista que usa el serializer custom

```python
# users/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

```python
# users/urls.py
from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### Payload resultante

```json
{
  "token_type": "access",
  "exp": 1700000000,
  "user_id": 1,
  "email": "admin@example.com",
  "is_staff": true,
  "role": "admin"
}
```

> **Nota:** No pongas datos sensibles (contraseñas, secretos) en los claims. El JWT se puede decodificar sin la clave secreta; la firma solo garantiza integridad, no confidencialidad.

---

## 2. Blacklist y Revocación de Tokens

El problema: los JWT son stateless, una vez emitidos no se pueden "invalidar" hasta que expiren. La app `token_blacklist` de SimpleJWT resuelve esto guardando en base de datos los tokens revocados.

### Instalación

```python
# src/core/settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework_simplejwt.token_blacklist',  # Agrega la app
]
```

```bash
# Después de agregar la app, migrar para crear las tablas
python manage.py migrate
```

### Configuración en settings.py

```python
# src/core/settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    # Rotar el refresh token en cada uso (emite uno nuevo y blacklistea el anterior)
    'ROTATE_REFRESH_TOKENS': True,

    # Blacklistear automáticamente el refresh token viejo al rotarlo
    'BLACKLIST_AFTER_ROTATION': True,
}
```

| Setting | Qué hace |
|---------|----------|
| `ROTATE_REFRESH_TOKENS` | Al usar `/token/refresh/`, devuelve un refresh token nuevo además del access |
| `BLACKLIST_AFTER_ROTATION` | El refresh token anterior se mete en la blacklist automáticamente |

### Vista de Logout (blacklistear manualmente)

```python
# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class LogoutView(APIView):
    """
    El cliente envía su refresh token y lo blacklisteamos.
    El access token seguirá vivo hasta que expire, pero sin refresh
    el usuario no puede renovarlo.
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
```

```python
# users/urls.py
urlpatterns = [
    # ...
    path('logout/', LogoutView.as_view(), name='logout'),
]
```

### Limpieza de tokens expirados

Los tokens blacklisteados se acumulan en la DB. SimpleJWT incluye un comando para limpiarlos:

```bash
# Elimina de la tabla los tokens que ya expiraron (no sirven para nada)
python manage.py flushexpiredtokens
```

> Podés automatizarlo con un cron job o django-celery-beat.

## Recursos

- [SimpleJWT — Customizing Token Claims](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html)
- [SimpleJWT — Blacklist App](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html)
