from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rfis', views.RFIViewSet)
router.register(r'rfi-evaluation-criteria', views.RFIEvaluationCriteriaViewSet)

urlpatterns = [
    path('rfi-types/types/', views.RFITypeView.as_view(), name='rfi-types'),
    path('', include(router.urls)),
]
