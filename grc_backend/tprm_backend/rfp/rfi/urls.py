from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import views
from .models import RFIEvaluationCriteria
from tprm_backend.core.tenant_utils import get_tenant_id_from_request

router = DefaultRouter()
router.register(r'rfis', views.RFIViewSet)
router.register(r'rfi-evaluation-criteria', views.RFIEvaluationCriteriaViewSet)

class EvaluationCriteriaRouterView(APIView):
    """Router view that handles DELETE with rfi_id and delegates other methods to ViewSet"""
    permission_classes = views.RFIEvaluationCriteriaViewSet.permission_classes
    
    def delete(self, request, *args, **kwargs):
        """Handle DELETE requests with rfi_id query param for bulk delete"""
        if 'rfi_id' in request.query_params:
            rfi_id = request.query_params.get('rfi_id')
            tenant_id = get_tenant_id_from_request(request)
            if not tenant_id:
                tenant_id = 1
            
            queryset = RFIEvaluationCriteria.objects.filter(rfi_id=rfi_id)
            if tenant_id:
                queryset = queryset.filter(tenant_id=tenant_id)
            
            count = queryset.count()
            queryset.delete()
            return Response({'deleted_count': count}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "DELETE requires a primary key or rfi_id query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request, *args, **kwargs):
        """Delegate GET requests to ViewSet list"""
        viewset = views.RFIEvaluationCriteriaViewSet()
        viewset.request = request
        viewset.format_kwarg = None
        viewset.action = 'list'
        return viewset.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Delegate POST requests to ViewSet create"""
        viewset = views.RFIEvaluationCriteriaViewSet()
        viewset.request = request
        viewset.format_kwarg = None
        viewset.action = 'create'
        return viewset.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """PUT requires pk"""
        return Response({"error": "PUT requires a primary key"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        """PATCH requires pk"""
        return Response({"error": "PATCH requires a primary key"}, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    path('rfi-types/types/', views.RFITypeView.as_view(), name='rfi-types'),
    # Custom router - handles DELETE with rfi_id, delegates others to ViewSet
    path('rfi-evaluation-criteria/', EvaluationCriteriaRouterView.as_view(), name='rfi-evaluation-criteria-router'),
    path('', include(router.urls)),
]
