from django.urls import path
from . import views

app_name = 'survey_app'

urlpatterns = [
    path('surveys/', views.SurveyList.as_view(), name='survey-list'),
    path('surveys/<int:pk>/', views.SurveyDetail.as_view(), name='survey-detail'),
    path('questions/', views.QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetail.as_view(), name='question-detail'),
    path('options/', views.OptionList.as_view(), name='option-list'),
    path('options/<int:pk>/', views.OptionDetail.as_view(), name='option-detail'),
    path('responses/', views.ResponseList.as_view(), name='response-list'),
    path('responses/<int:pk>/', views.ResponseDetail.as_view(), name='response-detail'),
]
