from django.urls import path
from . import views

app_name = 'survey_app'

urlpatterns = [
    path('surveys/', views.SurveyListView.as_view(),name= 'survey-list'),
    path('surveys/create/', views.SurveyCreateView.as_view(),name= 'survey-create' ),
    path('surveys/<int:pk>/', views.SurveyDetailView.as_view(),name= 'survey-detail'),
    path('survey/question/<int:pk>/update/',views.QuestionUpdateView.as_view(),name='question-update' ),
    path('survey/<int:survey_id>/question/create',views.QuestionCreateView.as_view(),name= 'question-create'),
    path('survey/question/<int:pk>/update',views.QuestionDetailView.as_view(),name='question-update' ),
    path('question/<int:question_id>/option/create',views.OptionCreateView.as_view(),name= 'option-create'),
    path('question/option/<int:pk>/update',views.OptionDetailView.as_view(),name='option-update' ),
    path('questions/<int:question_id>/answer/', views.AnswerQuestionView.as_view(), name='answer-question'),
]

