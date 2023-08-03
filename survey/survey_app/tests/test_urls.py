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

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from survey_app.models import Survey

class UpdateSurveyAPIViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a survey belonging to the test user
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)

        # Create a regular user (not the creator of the survey)
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

        # Create an authenticated client for the test user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_survey_url_resolves(self):
        url = reverse('update-survey', kwargs={'survey_id': self.survey.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_survey_by_creator(self):
        url = reverse('update-survey', kwargs={'survey_id': self.survey.id})
        updated_data = {'title': 'Updated Survey', 'creator': self.user.id}  # Add the 'creator' field
        response = self.client.put(url, updated_data)
        if response.status_code != status.HTTP_200_OK:
            print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.survey.refresh_from_db()
        self.assertEqual(self.survey.title, 'Updated Survey')

    def test_update_survey_by_non_creator(self):
        # Change the authenticated user to the non-creator user
        self.client.force_authenticate(user=self.other_user)

        url = reverse('update-survey', kwargs={'survey_id': self.survey.id})
        updated_data = {'title': 'Updated Survey'}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
