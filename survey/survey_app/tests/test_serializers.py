from django.test import TestCase
from rest_framework.exceptions import ValidationError
from survey_app.models import Survey, Question, Option, Answer
from survey_app.serializers import OptionSerializer, QuestionSerializer, SurveySerializer, AnswerSerializer
from django.contrib.auth.models import User

class OptionSerializerTestCase(TestCase):
    def test_option_serializer(self):
        survey = Survey.objects.create(title='Test Survey')
        question = Question.objects.create(text='Test Question', survey=survey)
        option_data = {'text': 'Test Option', 'question': question.id}
        serializer = OptionSerializer(data=option_data)
        self.assertTrue(serializer.is_valid())
        option = serializer.save()
        self.assertEqual(option.text, 'Test Option')
        self.assertEqual(option.question, question)

class QuestionSerializerTestCase(TestCase):
    def test_question_serializer(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Use the newly created user instance in survey_data
        survey_data = {
            'title': 'Test Survey',
            'creator': user,  # Pass the actual User instance
        }
        survey = Survey.objects.create(**survey_data)

        # Use the primary key of the newly created survey in question_data
        question_data = {
            'text': 'Test Question',
            'survey': survey.pk,  # Use the primary key of the newly created survey
        }
        serializer = QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid())  # Make sure the serializer is valid
        question = serializer.save()

        # Check if the question was saved correctly
        self.assertEqual(question.text, 'Test Question')
        self.assertEqual(question.survey, survey)

class SurveySerializerTestCase(TestCase):
    def test_survey_serializer(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        survey_data = {'title': 'Test Survey', 'creator': user.id}
        serializer = SurveySerializer(data=survey_data)
        self.assertTrue(serializer.is_valid())
        survey = serializer.save()
        self.assertEqual(survey.title, 'Test Survey')
        self.assertEqual(survey.creator, user)


class AnswerSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)
        self.question = Question.objects.create(survey=self.survey, text='Test Question')
        self.option = Option.objects.create(question=self.question, text='Test Option')

    def test_answer_serializer(self):
        class DummyRequest:
            user = self.user

        # Use the dummy request object in the serializer context
        answer_data = {'question': self.question.id, 'option': self.option.id}
        serializer = AnswerSerializer(data=answer_data, context={'request': DummyRequest()})

        self.assertTrue(serializer.is_valid())
        answer = serializer.save()

        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.option, self.option)

    def test_answer_submission_invalid_question(self):
        # Test submitting an answer with a non-existent question
        invalid_question_id = 999999
        answer_data = {'question': invalid_question_id, 'option': self.option.id}
        serializer = AnswerSerializer(data=answer_data, context={'request': None})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)

        self.assertIn("question", cm.exception.detail)

    def test_answer_submission_invalid_option(self):
        # Test submitting an answer with a non-existent option
        invalid_option_id = 999999
        answer_data = {'question': self.question.id, 'option': invalid_option_id}
        serializer = AnswerSerializer(data=answer_data, context={'request': None})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)

        self.assertIn("option", cm.exception.detail)
    # TODO
    def test_answer_submission_missing_question(self):
        # Attempt to create an answer without providing the 'question' field
        answer_data = {'option': self.option.id}
        serializer = AnswerSerializer(data=answer_data)

        # Check if the serializer is NOT valid, as it should raise a validation error
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)

        # Check if the error message contains the expected field error for 'question'
        self.assertIn('question', serializer.errors)

        # Ensure that the error message indicates that the 'question' field is required
        self.assertEqual(serializer.errors['question'][0].code, 'required')

    def test_answer_submission_missing_option(self):
        # Test submitting an answer without the 'option' field
        answer_data = {'question': self.question.id}
        serializer = AnswerSerializer(data=answer_data, context={'request': None})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)

        self.assertIn("option", cm.exception.detail)
