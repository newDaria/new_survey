from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Survey, Answer
from django.core.mail import send_mail


@receiver(post_save, sender=Survey)
def send_survey_creation_email(sender, instance, created, **kwargs):
    if created and instance.creator:
        # Get the creator's username if it exists, otherwise set it to 'Unknown'
        creator_username = instance.creator.username if instance.creator.username else "Unknown"

        # Compose the email message
        message = f'Hello {creator_username},\n\nYou have successfully created a new survey titled "{instance.title}".\n\nThank you for using our survey app!\n\nBest regards,\nThe Survey App Team'

        # Send the email
        send_mail(
            subject="Survey Created",
            message=message,
            from_email="surveyapp@example.com",  # Set the email sender address
            recipient_list=[instance.creator.email],  # Use the creator's email as the recipient
            fail_silently=False,
        )
