from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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


class Response(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.respondent.username} - {self.survey.title} - {self.question.text} - {self.option.text}"


