from django.urls import resolve
from django.test import TestCase
from django.urls import reverse

from survey_app.views import SurveyQuestionsView, QuestionOptionsView

class UrlsTest(TestCase):
    def test_survey_questions_url(self):
        url = reverse('survey-questions', kwargs={'survey_pk': 1})
        resolved_view = resolve(url).func
        self.assertEqual(resolved_view.view_class, SurveyQuestionsView)

    def test_question_options_url(self):
        url = reverse('question-options', kwargs={'question_pk': 1})
        resolved_view = resolve(url).func
        self.assertEqual(resolved_view.view_class, QuestionOptionsView)
