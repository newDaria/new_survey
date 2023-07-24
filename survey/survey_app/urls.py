from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurveyViewSet, QuestionViewSet, OptionViewSet, AnswerViewSet, SurveyQuestionsView, QuestionOptionsView

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




