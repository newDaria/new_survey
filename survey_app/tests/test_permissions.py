
# from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.test import APITestCase, APIRequestFactory
from survey_app.models import Survey, UserProfile
from survey_app.permissions import CanUpdateSurveyPermission
from survey_app.factories import SurveyFactory, QuestionFactory, OptionFactory, AnswerFactory,UserProfileFactory


class CanUpdateSurveyPermissionAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = UserProfileFactory()
        self.other_user = UserProfileFactory()

        # Create a test survey for the test user
        self.survey = SurveyFactory(creator=self.user)

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
