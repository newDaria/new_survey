from django.test import TestCase
from rest_framework.test import APITestCase
from django.core import mail
from survey_app.models import Survey, Question, Option, Answer, UserProfile
from survey_app.cron import DailySurveySubmissionsEmail
from survey_app.factories import SurveyFactory, QuestionFactory, OptionFactory, AnswerFactory,UserProfileFactory

class DailySurveySubmissionsEmailTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = UserProfileFactory()

        # Create a test survey
        self.survey = SurveyFactory(creator=self.user)
    def test_daily_survey_submissions_email(self):
        # Create a test answer for the survey
        self.question = QuestionFactory(survey=self.survey)
        self.option = OptionFactory(question=self.question)
        self.answer = AnswerFactory(question=self.question, option=self.option, creator=self.user)

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
