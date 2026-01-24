from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rpqs', views.RPQViewSet)
router.register(r'rpq-evaluation-criteria', views.RPQEvaluationCriteriaViewSet)

urlpatterns = [
    path('rpq-types/types/', views.RPQTypeView.as_view(), name='rpq-types'),
    path('', include(router.urls)),
]
