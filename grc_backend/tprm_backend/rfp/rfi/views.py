from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from .models import RFI, RFIEvaluationCriteria
from .serializers import RFISerializer, RFICreateSerializer, RFIListSerializer, RFIEvaluationCriteriaSerializer
from tprm_backend.core.tenant_utils import (
    get_tenant_id_from_request,
    filter_queryset_by_tenant,
    get_tenant_aware_queryset,
)


class RFIViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing RFIs
    """
    queryset = RFI.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['rfi_title', 'description', 'rfi_number']
    ordering_fields = ['created_at', 'updated_at', 'submission_deadline', 'rfi_title']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return RFIListSerializer
        elif self.action == 'create':
            return RFICreateSerializer
        return RFISerializer
    
    def get_queryset(self):
        """Filter queryset by tenant"""
        queryset = super().get_queryset()
        tenant_id = get_tenant_id_from_request(self.request)
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Override list to handle tenant filtering"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Override create to handle tenant and user assignment"""
        tenant_id = get_tenant_id_from_request(request)
        if not tenant_id:
            return Response(
                {"error": "Tenant context not found. Cannot create RFI without tenant."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get or create admin user for development
        from django.contrib.auth.models import User
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        
        # Add tenant_id to data if not present
        if 'tenant_id' not in data and 'tenant' not in data:
            data['tenant_id'] = tenant_id
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=admin_user.id, tenant_id=tenant_id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            import traceback
            print(f"Exception during RFI creation: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Override update to handle tenant filtering"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RFIEvaluationCriteriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing RFI evaluation criteria
    """
    queryset = RFIEvaluationCriteria.objects.all()
    serializer_class = RFIEvaluationCriteriaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by RFI and tenant"""
        queryset = super().get_queryset()
        rfi_id = self.request.query_params.get('rfi_id', None)
        tenant_id = get_tenant_id_from_request(self.request)
        
        if rfi_id:
            queryset = queryset.filter(rfi_id=rfi_id)
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to handle bulk delete by rfi_id"""
        rfi_id = request.query_params.get('rfi_id', None)
        if rfi_id and not kwargs.get('pk'):
            # Bulk delete all criteria for this RFI
            queryset = self.get_queryset().filter(rfi_id=rfi_id)
            count = queryset.count()
            queryset.delete()
            return Response({'deleted_count': count}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Override create to set tenant and created_by"""
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
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        
        data = request.data.copy()
        if 'tenant_id' not in data:
            data['tenant_id'] = tenant_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=admin_user.id, tenant_id=tenant_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RFITypeView(APIView):
    """API endpoint for getting RFI types"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get list of unique RFI types from existing RFIs"""
        tenant_id = get_tenant_id_from_request(request)
        queryset = RFI.objects.all()
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        rfi_types = queryset.values_list('rfi_type', flat=True).distinct().order_by('rfi_type')
        return Response({
            'success': True,
            'rfi_types': list(rfi_types)
        })
