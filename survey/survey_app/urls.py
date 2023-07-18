from django.urls import path
from . import views

app_name = 'survey_app'

urlpatterns = [
    # done
    path('surveys/', views.SurveyListView.as_view(),name= 'survey-list'),
    # done
    path('surveys/create/', views.SurveyCreateView.as_view(),name= 'survey-create' ),
    # done can see title and questions
    path('surveys/<int:pk>/', views.SurveyDetailView.as_view(),name= 'survey-detail'),
    # dont need since we can see it at survey
    # path('questions/<int:survey_id>/', views.QuestionDetailView.as_view(),name='question-list'),
    # done
    path('survey/question/<int:pk>/update/',views.QuestionUpdateView.as_view(),name='question-update' ),
    # done
    path('survey/<int:survey_id>/question/create',views.QuestionCreateView.as_view(),name= 'question-create'),
    # done
    path('survey/question/<int:pk>/update',views.QuestionDetailView.as_view(),name='question-update' ),
    # done
    path('question/<int:question_id>/option/create',views.OptionCreateView.as_view(),name= 'option-create'),
    # done
    path('question/option/<int:pk>/update',views.OptionDetailView.as_view(),name='option-update' ),
    # doesnt work
    path('answer/<int:question_id>/update/',views.AnswerDetailView.as_view(),name='answer-update' ),


]

