from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Survey, Answer
from anymail.message import AnymailMessage
from django.utils import timezone

@receiver(post_save, sender=Survey)
def send_survey_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Survey Created'
        message = f'Hello {instance.creator.username},\n\nYou have successfully created a new survey titled "{instance.title}".\n\nThank you for using our survey app!\n\nBest regards,\nThe Survey App Team'

        # Use AnymailMessage to create the email
        email = AnymailMessage(
            subject=subject,
            body=message,
            to=[instance.creator.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
        )

        # Send the email using Anymail's send method
        email.send()

# @receiver(post_save, sender=Answer)
# def enforce_submission_limit(sender, instance, created, **kwargs):
#     if created:
#         user = instance.creator
#         if user:
#             # Get the current date
#             today = timezone.now().date()
#
#             # Count the number of answers submitted by the user on the current date
#             user_submission_count = Answer.objects.filter(creator=user, created_at__date=today).count()
#
#             if user_submission_count > 5:
#                 # Restrict the user from submitting more than 5 answers per day
#                 raise ValueError("You have already submitted the maximum allowed answers for today.")