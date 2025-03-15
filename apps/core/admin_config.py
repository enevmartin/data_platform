# apps/core/admin_config.py
from django.apps import AppConfig
from django.contrib import admin

def customize_admin_site():
    from django.conf import settings
    admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Django Administration')
    admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Django Site Admin')
    admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Site Administration')