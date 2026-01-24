from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Auction, AuctionEvaluationCriteria
from .serializers import AuctionSerializer, AuctionCreateSerializer, AuctionListSerializer, AuctionEvaluationCriteriaSerializer
from tprm_backend.core.tenant_utils import get_tenant_id_from_request


class AuctionViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Auctions"""
    queryset = Auction.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['auction_title', 'description', 'auction_number']
    ordering_fields = ['created_at', 'updated_at', 'submission_deadline', 'auction_title']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return AuctionListSerializer
        elif self.action == 'create':
            return AuctionCreateSerializer
        return AuctionSerializer
    
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
                {"error": "Tenant context not found. Cannot create Auction without tenant."},
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
            print(f"Exception during Auction creation: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AuctionEvaluationCriteriaViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Auction evaluation criteria"""
    queryset = AuctionEvaluationCriteria.objects.all()
    serializer_class = AuctionEvaluationCriteriaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        auction_id = self.request.query_params.get('auction_id', None)
        tenant_id = get_tenant_id_from_request(self.request)
        
        if auction_id:
            queryset = queryset.filter(auction_id=auction_id)
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to handle bulk delete by auction_id"""
        auction_id = request.query_params.get('auction_id', None)
        if auction_id and not kwargs.get('pk'):
            queryset = self.get_queryset().filter(auction_id=auction_id)
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


class AuctionTypeView(APIView):
    """API endpoint for getting Auction types"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get list of unique Auction types from existing Auctions"""
        tenant_id = get_tenant_id_from_request(request)
        queryset = Auction.objects.all()
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        auction_types = queryset.values_list('auction_type', flat=True).distinct().order_by('auction_type')
        return Response({
            'success': True,
            'auction_types': list(auction_types)
        })
