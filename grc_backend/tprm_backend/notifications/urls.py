# notifications/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import NotificationViewSet, notification_stats

router = SimpleRouter()
router.register(r'', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', notification_stats, name='notification-stats'),
]
