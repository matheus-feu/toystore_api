from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


@extend_schema(tags=['authentication'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['authentication'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['authentication'])
class CustomTokenVerifyView(TokenVerifyView):
    pass
