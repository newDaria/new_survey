from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from survey_app.views import SurveyQuestionsView, QuestionOptionsView
from survey_app.models import Survey, UserProfile
from django.test import TestCase




from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from survey_app.views import SurveyQuestionsView, QuestionOptionsView

from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from survey_app.views import SurveyQuestionsView, QuestionOptionsView

from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from survey_app.views import SurveyQuestionsView, QuestionOptionsView

class UrlsTest(APITestCase):
    def test_survey_questions_url(self):
        url = reverse('survey-questions', kwargs={'survey_pk': 1})
        resolved_view = resolve(url).func
        expected_view_name = SurveyQuestionsView.as_view({'get': 'list'}).__name__
        self.assertEqual(resolved_view.__name__, expected_view_name)

    def test_question_options_url(self):
        url = reverse('question-options', kwargs={'question_pk': 1})
        resolved_view = resolve(url).func
        expected_view_name = QuestionOptionsView.as_view({'get': 'list', 'post': 'create'}).__name__
        self.assertEqual(resolved_view.__name__, expected_view_name)


class UpdateSurveyAPIViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)
        self.other_user = UserProfile.objects.create_user(username='otheruser', password='otherpassword', email='other_test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_update_survey_url_resolves(self):
        url = reverse('update-survey', kwargs={'survey_id': self.survey.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_survey_by_creator(self):
        url = reverse('update-survey', kwargs={'survey_id': self.survey.id})
        updated_data = {'title': 'Updated Survey', 'creator': self.user.id}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.survey.refresh_from_db()
        self.assertEqual(self.survey.title, 'Updated Survey')

    def test_update_survey_by_non_creator(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('update-survey', kwargs={'survey_id': self.survey.id})
        updated_data = {'title': 'Updated Survey'}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
