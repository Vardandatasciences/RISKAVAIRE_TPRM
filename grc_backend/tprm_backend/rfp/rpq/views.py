from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import RPQ, RPQEvaluationCriteria
from .serializers import RPQSerializer, RPQCreateSerializer, RPQListSerializer, RPQEvaluationCriteriaSerializer
from tprm_backend.core.tenant_utils import get_tenant_id_from_request


class RPQViewSet(viewsets.ModelViewSet):
    """API endpoint for managing RPQs"""
    queryset = RPQ.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['rpq_title', 'description', 'rpq_number']
    ordering_fields = ['created_at', 'updated_at', 'submission_deadline', 'rpq_title']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return RPQListSerializer
        elif self.action == 'create':
            return RPQCreateSerializer
        return RPQSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_id = get_tenant_id_from_request(self.request)
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        tenant_id = get_tenant_id_from_request(request)
        if not tenant_id:
            return Response(
                {"error": "Tenant context not found. Cannot create RPQ without tenant."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from django.contrib.auth.models import User
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin', email='admin@example.com', password='admin123'
            )
        
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        if 'tenant_id' not in data:
            data['tenant_id'] = tenant_id
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=admin_user.id, tenant_id=tenant_id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            import traceback
            print(f"Exception during RPQ creation: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RPQEvaluationCriteriaViewSet(viewsets.ModelViewSet):
    """API endpoint for managing RPQ evaluation criteria"""
    queryset = RPQEvaluationCriteria.objects.all()
    serializer_class = RPQEvaluationCriteriaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        rpq_id = self.request.query_params.get('rpq_id', None)
        tenant_id = get_tenant_id_from_request(self.request)
        
        if rpq_id:
            queryset = queryset.filter(rpq_id=rpq_id)
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to handle bulk delete by rpq_id"""
        rpq_id = request.query_params.get('rpq_id', None)
        if rpq_id and not kwargs.get('pk'):
            queryset = self.get_queryset().filter(rpq_id=rpq_id)
            count = queryset.count()
            queryset.delete()
            return Response({'deleted_count': count}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        tenant_id = get_tenant_id_from_request(request)
        if not tenant_id:
            return Response(
                {"error": "Tenant context not found."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from django.contrib.auth.models import User
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin', email='admin@example.com', password='admin123'
            )
        
        data = request.data.copy()
        if 'tenant_id' not in data:
            data['tenant_id'] = tenant_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=admin_user.id, tenant_id=tenant_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RPQTypeView(APIView):
    """API endpoint for getting RPQ types"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get list of unique RPQ types from existing RPQs"""
        tenant_id = get_tenant_id_from_request(request)
        queryset = RPQ.objects.all()
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        rpq_types = queryset.values_list('rpq_type', flat=True).distinct().order_by('rpq_type')
        return Response({
            'success': True,
            'rpq_types': list(rpq_types)
        })
