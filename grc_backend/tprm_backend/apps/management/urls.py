"""
URL configuration for management app
"""

from django.urls import path, include
from django.http import JsonResponse
from datetime import datetime
from rest_framework.routers import DefaultRouter
from .views import AllVendorsListView, VendorDetailView
from . import views
app_name = 'management'
management_router = DefaultRouter()
management_router.register(r'temp-vendors', views.TempVendorManagementViewSet, basename='temp-vendors')

def health_check(request):
    """Simple health check to verify URLs are working"""
    return JsonResponse({'status': 'ok', 'message': 'Management app URLs are working'})

def test_endpoint(request):
    """Test endpoint to verify management URLs are loaded"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Management URLs are loaded',
        'timestamp': str(datetime.now()),
        'endpoints': {
            'health': '/api/v1/management/health/',
            'vendors_all': '/api/v1/management/vendors/all/',
            'vendor_detail': '/api/v1/management/vendors/<vendor_code>/'
        }
    })

urlpatterns = [
    path('test/', test_endpoint, name='management-test'),
    path('health/', health_check, name='health-check'),
    path('vendors/all/', AllVendorsListView.as_view(), name='all-vendors-list'),
    path('vendors/<str:vendor_code>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('', include(management_router.urls)),
]
