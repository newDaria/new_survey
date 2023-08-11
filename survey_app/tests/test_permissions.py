from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.test import APIRequestFactory
from survey_app.models import Survey
from survey_app.permissions import CanUpdateSurveyPermission

class CanUpdateSurveyPermissionTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='testpassword')

        # Create a test survey for the test user
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)

        # Create an API request factory
        self.factory = APIRequestFactory()

    def test_can_update_survey_permission(self):
        # Create a PUT request to update the test survey
        url = f'/surveys/{self.survey.pk}/update/'
        request = self.factory.put(url)

        # Assign the test user to the request as the authenticated user
        request.user = self.user

        # Create an API view with the permission class
        view = APIView()
        view.kwargs = {'survey_id': self.survey.pk}
        permission = CanUpdateSurveyPermission()

        # Check if the test user has permission to update the survey
        self.assertTrue(permission.has_permission(request, view))

    def test_cannot_update_survey_permission_other_user(self):
        # Create a PUT request to update the test survey
        url = f'/surveys/{self.survey.pk}/update/'
        request = self.factory.put(url)

        # Assign the other user to the request as the authenticated user
        request.user = self.other_user

        # Create an API view with the permission class
        view = APIView()
        view.kwargs = {'survey_id': self.survey.pk}
        permission = CanUpdateSurveyPermission()

        # Check if the other user does not have permission to update the survey
        self.assertFalse(permission.has_permission(request, view))
