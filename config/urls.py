from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.core.admin_views import admin_dashboard
from apps.core.views import HealthCheckView  # Import HealthCheckView

urlpatterns = [




    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('', HealthCheckView.as_view(), name='health_check'),  # Map root URL to HealthCheckView
    path('admin/', admin.site.urls),
    path('api/', include('apps.core.urls')),  # Existing pattern for core app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Only include debug toolbar URLs in debug mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
