from django.test import TestCase
from survey_app.models import Survey, Question, Option, Answer
from survey_app.serializers import OptionSerializer, QuestionSerializer, SurveySerializer, AnswerSerializer
from django.contrib.auth.models import User

class OptionSerializerTestCase(TestCase):
    def test_option_serializer(self):
        # Create a Survey object first
        survey = Survey.objects.create(title='Test Survey')

        # Create the Question object and associate it with the survey
        question = Question.objects.create(text='Test Question', survey=survey)

        # Now, create the Option object with the associated Question
        option_data = {'text': 'Test Option', 'question': question.id}
        serializer = OptionSerializer(data=option_data)
        if not serializer.is_valid():
            print(serializer.errors)
            print(f'text: {option_data["text"]}')
        self.assertTrue(serializer.is_valid())

class QuestionSerializerTestCase(TestCase):
    def test_question_serializer(self):
        survey = Survey.objects.create(title='Test Survey')

        # Use the primary key of the newly created survey in question_data
        question_data = {
            'text': 'Test Question',
            'survey': survey.pk,  # Use the primary key of the newly created survey
        }
        serializer = QuestionSerializer(data=question_data)
        if not serializer.is_valid():
            print(serializer.errors)
            print(f'text: {question_data["text"]}')
        self.assertTrue(serializer.is_valid())

class SurveySerializerTestCase(TestCase):
    def test_survey_serializer(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')

        survey_data = {'title': 'Test Survey', 'creator': user.id}  # Provide the creator's ID
        serializer = SurveySerializer(data=survey_data)
        self.assertTrue(serializer.is_valid())
        survey = serializer.save()

        self.assertEqual(survey.title, 'Test Survey')
        self.assertEqual(survey.creator, user)
class AnswerSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)

    def test_answer_serializer(self):
        question = Question.objects.create(survey=self.survey, text='Test Question')
        option = Option.objects.create(question=question, text='Test Option')
        answer_data = {'question': question.pk, 'option': option.pk}  # Use pk values instead of objects
        serializer = AnswerSerializer(data=answer_data)
        if not serializer.is_valid():
            print(serializer.errors)
            print(f'question: {answer_data["question"]}')
            print(f'option: {answer_data["option"]}')
        self.assertTrue(serializer.is_valid())
        answer = serializer.save()

        self.assertEqual(answer.question, question)
        self.assertEqual(answer.option, option)