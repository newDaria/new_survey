from django.urls import resolve
from django.test import TestCase
from django.urls import reverse
from survey_app.views import SurveyQuestionsView, QuestionOptionsView, UpdateSurveyAPIView
from survey_app.views import UpdateSurveyAPIView


class UrlsTest(TestCase):
    def test_survey_questions_url(self):
        url = reverse('survey-questions', kwargs={'survey_pk': 1})
        resolved_view = resolve(url).func
        self.assertEqual(resolved_view.__name__, 'SurveyQuestionsView')

    def test_question_options_url(self):
        url = reverse('question-options', kwargs={'question_pk': 1})
        resolved_view = resolve(url).func
        self.assertEqual(resolved_view.__name__, 'QuestionOptionsView')
    # TODO
    def test_update_survey_url(self):
        url = reverse('update-survey', kwargs={'survey_id': 1})
        resolved_view = resolve(url).func
        print(f"Resolved View: {resolved_view.__name__}")  # Add this print statement
        self.assertEqual(resolved_view.__name__, 'UpdateSurveyAPIView')


