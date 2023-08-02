from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from survey_app.models import Survey
from survey_app.signals import send_survey_creation_email

class SurveyCreationEmailTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_send_survey_creation_email(self):
        # Create a test survey
        survey = Survey.objects.create(title='Test Survey', creator=self.user)

        # Clear the mail.outbox before calling the signal to ensure only the email sent in this test is checked.
        mail.outbox = []

        # Call the signal directly
        send_survey_creation_email(sender=Survey, instance=survey, created=True)

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the email content
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Survey Created')
        self.assertIn(f'Hello {self.user.username},', email.body)
        self.assertIn(f'You have successfully created a new survey titled "{survey.title}".', email.body)
        self.assertIn('Thank you for using our survey app!', email.body)
        self.assertIn('Best regards,', email.body)
        self.assertIn('The Survey App Team', email.body)

        # Check the email recipient
        self.assertEqual(email.to, [self.user.email])
