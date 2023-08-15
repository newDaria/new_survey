from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    SurveyViewSet,
    QuestionViewSet,
    OptionViewSet,
    AnswerViewSet,
    SurveyQuestionsView,
    QuestionOptionsView,
    UpdateSurveyAPIView,
    SignupAPIView,
    LoginAPIView,
    LogoutAPIView,
)

from rest_framework.exceptions import PermissionDenied


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'surveys', SurveyViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('surveys/<int:survey_pk>/questions/', SurveyQuestionsView.as_view({'get': 'list'}), name='survey-questions'),
    path('questions/<int:question_pk>/options/', QuestionOptionsView.as_view({'get': 'list', 'post': 'create'}), name='question-options'),

    # Add the URL pattern for UpdateSurveyAPIView
    path('surveys/<int:survey_id>/update/', UpdateSurveyAPIView.as_view(), name='update-survey'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('auth/', include('djoser.urls')),


]

# GET /surveys/
# POST /surveys/
# PUT /surveys/<survey_id>/

# GET /questions/
# POST /questions/
# PUT /questions/<question_id>/


# GET /options/
# POST /options/
# PUT /options/<option_id>/

# GET /answers/
# POST /answers/
# PUT /answers/<option_id>/




