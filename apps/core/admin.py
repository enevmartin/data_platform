# apps/core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

from apps.core.models import Dataset, DataFile, Institution


class DataFileInline(admin.TabularInline):
    model = DataFile
    extra = 0
    fields = ('name', 'file_type', 'status', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True
    can_delete = False  # For data integrity
    max_num = 10  # Limit for performance


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution_link', 'file_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'institution', 'created_at')
    search_fields = ('name', 'description', 'institution__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DataFileInline]
    actions = ['mark_active', 'mark_inactive']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optimize by prefetching related institution and annotating with file count
        return queryset.select_related('institution').annotate(
            file_count=Count('datafile')
        )

    def institution_link(self, obj):
        url = reverse('admin:core_institution_change', args=[obj.institution.id])
        return format_html('<a href="{}">{}</a>', url, obj.institution.name)

    institution_link.short_description = 'Institution'

    def file_count(self, obj):
        return obj.file_count

    file_count.admin_order_field = 'file_count'
    file_count.short_description = 'Number of Files'

    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} datasets marked as active.")

    mark_active.short_description = "Mark selected datasets as active"

    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} datasets marked as inactive.")

    mark_inactive.short_description = "Mark selected datasets as inactive"


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'dataset_count', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optimize by annotating with dataset count
        return queryset.annotate(dataset_count=Count('datasets'))

    def dataset_count(self, obj):
        return obj.dataset_count

    dataset_count.admin_order_field = 'dataset_count'
    dataset_count.short_description = 'Number of Datasets'


@admin.register(DataFile)
class DataFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'dataset_link', 'file_type', 'status', 'created_at')
    list_filter = ('file_type', 'status', 'created_at')
    search_fields = ('name', 'dataset__name')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optimize by prefetching related dataset and its institution
        return queryset.select_related('dataset__institution')

    def dataset_link(self, obj):
        url = reverse('admin:core_dataset_change', args=[obj.dataset.id])
        return format_html('<a href="{}">{}</a>', url, obj.dataset.name)

    dataset_link.short_description = 'Dataset'