# apps/core/admin_views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum
from apps.core.models import Dataset, DataFile, Institution

@staff_member_required
def admin_dashboard(request):
    """Custom admin dashboard with key metrics"""
    context = {
        'dataset_count': Dataset.objects.count(),
        'active_dataset_count': Dataset.objects.filter(is_active=True).count(),
        'institution_count': Institution.objects.count(),
        'datafile_count': DataFile.objects.count(),
        'recent_datasets': Dataset.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin/dashboard.html', context)