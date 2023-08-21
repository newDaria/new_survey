from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from survey_app.models import Survey, Question, Option, Answer
from survey_app.models import UserProfile
from survey_app.factories import SurveyFactory, QuestionFactory, OptionFactory, AnswerFactory,UserProfileFactory


class SurveyQuestionsViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfileFactory()
        self.client.force_authenticate(user=self.user)
        self.survey = SurveyFactory(creator=self.user)
        self.question = QuestionFactory(survey=self.survey)
        self.option = OptionFactory(question=self.question)

    def test_list_survey_questions(self):
        url = reverse('survey-questions', kwargs={'survey_pk': self.survey.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['survey']['title'], 'Test Survey')
        self.assertEqual(len(response.data['questions']), 1)
        self.assertEqual(response.data['questions'][0]['text'], 'Test Question')

class QuestionOptionsViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfileFactory()
        self.client.force_authenticate(user=self.user)
        self.survey = SurveyFactory(creator=self.user)
        self.question = QuestionFactory(survey=self.survey)

    def test_list_question_options(self):
        url = reverse('question-options', kwargs={'question_pk': self.question.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question']['text'], 'Test Question')
        self.assertEqual(len(response.data['options']), 0)

    def test_create_question_option(self):
        url = reverse('question-options', kwargs={'question_pk': self.question.pk})
        data = {'text': 'Test Option', 'question': self.question.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.question.option_set.count(), 1)
        self.assertEqual(self.question.option_set.first().text, 'Test Option')
