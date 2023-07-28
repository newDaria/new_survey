from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        creator_username = self.creator.username if self.creator else "Unknown"
        survey_title = self.question.survey.title if self.question.survey else "Unknown"
        question_text = self.question.text if self.question else "Unknown"
        option_text = self.option.text if self.option else "Unknown"

        return f"{creator_username} - {survey_title} - {question_text} - {option_text}"
