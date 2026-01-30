"""
Vendor Questionnaire URLs
"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import QuestionnaireViewSet, QuestionnaireQuestionViewSet, QuestionnaireAssignmentViewSet, QuestionnaireResponseViewSet

# Create router for ViewSets
router = SimpleRouter()
router.register(r'questionnaires', QuestionnaireViewSet, basename='questionnaire')
router.register(r'questions', QuestionnaireQuestionViewSet, basename='questionnaire-question')
router.register(r'assignments', QuestionnaireAssignmentViewSet, basename='questionnaire-assignment')
router.register(r'responses', QuestionnaireResponseViewSet, basename='questionnaire-response')

urlpatterns = [
    # Include all router URLs
    path('', include(router.urls)),
]
