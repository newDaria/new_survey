from django.core.mail import send_mail
from django.conf import settings
from survey_app.models import Survey, Answer
from django_cron import CronJobBase, Schedule

class DailySurveySubmissionsEmail(CronJobBase):
    RUN_EVERY_MINS = 2  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'survey_app.my_cron_job'

    def do(self):
        surveys = Survey.objects.all()

        for survey in surveys:
            submission_count = Answer.objects.filter(question__survey=survey).count()

            # Create the email content
            subject = 'Daily Survey Submissions Report'
            message = f'Hello {survey.creator.username},\n\nYou have received {submission_count} submissions for your survey "{survey.title}" today.\n\nThank you for using our survey app!\n\nBest regards,\nThe Survey App Team'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [survey.creator.email]

            # Send the email using Anymail's send_mail method
            send_mail(subject, message, from_email, recipient_list)


