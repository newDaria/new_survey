from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Survey
from anymail.message import AnymailMessage

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
