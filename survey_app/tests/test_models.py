from django.test import TestCase
from survey_app.models import Survey, Question, Option, Answer
from django.contrib.auth.models import User

class SurveyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)

    def test_survey_title(self):
        self.assertEqual(self.survey.title, 'Test Survey')

    def test_survey_creator(self):
        self.assertEqual(self.survey.creator, self.user)


class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)
        self.question = Question.objects.create(survey=self.survey, text='Test Question')

    def test_question_text(self):
        self.assertEqual(self.question.text, 'Test Question')

    def test_question_survey(self):
        self.assertEqual(self.question.survey, self.survey)


class OptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)
        self.question = Question.objects.create(survey=self.survey, text='Test Question')
        self.option = Option.objects.create(question=self.question, text='Test Option')

    def test_option_text(self):
        self.assertEqual(self.option.text, 'Test Option')

    def test_option_question(self):
        self.assertEqual(self.option.question, self.question)


class AnswerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)
        self.question = Question.objects.create(survey=self.survey, text='Test Question')
        self.option = Option.objects.create(question=self.question, text='Test Option')
        self.answer = Answer.objects.create(question=self.question, option=self.option, creator=self.user)

    def test_answer_question(self):
        self.assertEqual(self.answer.question, self.question)

    def test_answer_option(self):
        self.assertEqual(self.answer.option, self.option)

    def test_answer_creator(self):
        self.assertEqual(self.answer.creator, self.user)
