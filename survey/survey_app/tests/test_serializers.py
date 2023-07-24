from django.test import TestCase
from survey_app.models import Survey, Question, Option, Answer
from survey_app.serializers import OptionSerializer, QuestionSerializer, SurveySerializer, AnswerSerializer

class OptionSerializerTestCase(TestCase):
    def test_option_serializer(self):
        option_data = {'text': 'Test Option'}
        serializer = OptionSerializer(data=option_data)
        self.assertTrue(serializer.is_valid())
        option = serializer.save()

        self.assertEqual(option.text, 'Test Option')

class QuestionSerializerTestCase(TestCase):
    def test_question_serializer(self):
        question_data = {'text': 'Test Question'}
        serializer = QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid())
        question = serializer.save()

        self.assertEqual(question.text, 'Test Question')

class SurveySerializerTestCase(TestCase):
    def test_survey_serializer(self):
        survey_data = {'title': 'Test Survey'}
        serializer = SurveySerializer(data=survey_data)
        self.assertTrue(serializer.is_valid())
        survey = serializer.save()

        self.assertEqual(survey.title, 'Test Survey')

class AnswerSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)

    def test_answer_serializer(self):
        question = Question.objects.create(survey=self.survey, text='Test Question')
        option = Option.objects.create(question=question, text='Test Option')
        answer_data = {'question': question.id, 'option': option.id}
        serializer = AnswerSerializer(data=answer_data)
        self.assertTrue(serializer.is_valid())
        answer = serializer.save()

        self.assertEqual(answer.question, question)
        self.assertEqual(answer.option, option)

