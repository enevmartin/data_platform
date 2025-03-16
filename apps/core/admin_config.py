# Fixed admin_config.py
from django.contrib import admin
from django.conf import settings
from apps.core.models import DataFile, Dataset, Institution


def customize_admin_site():
    # Site customization
    admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Data Platform Administration')
    admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Data Platform Admin')
    admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Site Administration')

    # # # Model admin classes
    # # class DataFileAdmin(admin.ModelAdmin):
    # #     list_display = ('name', 'file_type', 'status', 'created_at')
    # #     list_filter = ('file_type', 'status')
    # #     search_fields = ('name',)
    # #     readonly_fields = ('created_at', 'updated_at')
    # #
    # #     def get_queryset(self, request):
    # #         qs = super().get_queryset(request)
    # #         return qs.select_related('dataset')
    #
    # # Register models
    # admin.site.register(DataFile, DataFileAdmin)
    #
    # # Similar for Dataset and Institution - implement these