from django.core.mail import send_mail
from django.conf import settings
from survey_app.models import Survey, Answer
from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = "Daily Survey Submissions Report."

    def execute(self):
        surveys = Survey.objects.all()

        for survey in surveys:
            submission_count = Answer.objects.filter(question__survey=survey).count()

            # Create the email content
            subject = 'Daily Survey Submissions Report'
            message = f'Hello {survey.creator.username},\n\nYou have received {submission_count} submissions for your survey "{survey.title}" today.\n\nThank you for using our survey app!\n\nBest regards,\nThe Survey App Team'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [survey.creator.email]
            print('Sample is working')

            # Send the email using Django's send_mail function
            send_mail(subject, message, from_email, recipient_list)
