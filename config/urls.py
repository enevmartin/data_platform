from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.core.urls')),  # Changed from 'core.urls' to 'apps.core.urls'
    # path('api/data/', include('apps.data_manager.urls')),  # If this app exists, update path here too
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)