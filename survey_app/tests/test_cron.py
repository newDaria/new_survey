from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from survey_app.models import Survey, Question, Option, Answer, UserProfile
from survey_app.cron import DailySurveySubmissionsEmail

class DailySurveySubmissionsEmailTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = UserProfile.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        # Create a test survey
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)

    def test_daily_survey_submissions_email(self):
        # Create a test answer for the survey
        question = Question.objects.create(survey=self.survey, text='Test Question')
        option = Option.objects.create(question=question, text='Test Option')
        answer = Answer.objects.create(question=question, option=option)

        # Clear the mail.outbox before running the cron job to ensure only the email sent in this test is checked.
        mail.outbox = []

        # Call the `do` method of the cron job directly
        cron_job = DailySurveySubmissionsEmail()
        cron_job.do()

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the email content
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Daily Survey Submissions Report')
        self.assertIn(f'Hello {self.user.username},', email.body)
        self.assertIn(f'You have received 1 submissions for your survey "{self.survey.title}" today.', email.body)
        self.assertIn('Thank you for using our survey app!', email.body)
        self.assertIn('Best regards,', email.body)
        self.assertIn('The Survey App Team', email.body)

        # Check the email recipient
        self.assertEqual(email.to, [self.user.email])
