from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class HealthCheckView(views.APIView):
    """
    API endpoint for system health checks.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # Check database connection
        db_healthy = True
        try:
            connections['default'].cursor()
        except OperationalError:
            db_healthy = False

        # Check cache connection
        cache_healthy = True
        try:
            cache.set('health_check', 'ok', 1)
            cache_value = cache.get('health_check')
            if cache_value != 'ok':
                cache_healthy = False
        except Exception:
            cache_healthy = False

        # Overall health status
        is_healthy = db_healthy and cache_healthy

        return Response({
            'status': 'healthy' if is_healthy else 'unhealthy',
            'database': 'connected' if db_healthy else 'disconnected',
            'cache': 'connected' if cache_healthy else 'disconnected',
        }, status=status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE)