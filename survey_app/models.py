from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_created = models.DateTimeField(null=True, default=timezone.now)
    is_active = models.BooleanField(default=True)  # Add this field
    is_staff = models.BooleanField(default=False)  # Add this field

    def user_profile_pic_path(instance, filename):
        # Generate a dynamic path to store the uploaded profile picture
        return f'profile_pics/{filename}'

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class Survey(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = [
            ('can_update_survey', 'Can update survey'),
        ]

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        creator_username = self.creator.username if self.creator else "Unknown"
        survey_title = self.question.survey.title if self.question.survey else "Unknown"
        question_text = self.question.text if self.question else "Unknown"
        option_text = self.option.text if self.option else "Unknown"

        return f"{creator_username} - {survey_title} - {question_text} - {option_text}"

    @staticmethod
    def user_submission_count_for_day(user, date):
        return Answer.objects.filter(creator=user, created_at__date=date).count()
