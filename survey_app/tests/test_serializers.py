from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from survey_app.models import Survey, Question, Option, Answer
from survey_app.serializers import OptionSerializer, QuestionSerializer, SurveySerializer, AnswerSerializer
from survey_app.models import UserProfile

class OptionSerializerAPITestCase(APITestCase):
    def test_option_serializer(self):
        survey = Survey.objects.create(title='Test Survey')
        question = Question.objects.create(text='Test Question', survey=survey)
        option_data = {'text': 'Test Option', 'question': question.id}
        serializer = OptionSerializer(data=option_data)
        self.assertTrue(serializer.is_valid())
        option = serializer.save()
        self.assertEqual(option.text, 'Test Option')
        self.assertEqual(option.question, question)

class QuestionSerializerAPITestCase(APITestCase):
    def test_question_serializer(self):
        user = UserProfile.objects.create_user(username='testuser', password='testpassword',
                                               email='testuser@example.com')
        survey_data = {
            'title': 'Test Survey',
            'creator': user,
        }
        survey = Survey.objects.create(**survey_data)

        question_data = {
            'text': 'Test Question',
            'survey': survey.pk,
        }
        serializer = QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid())
        question = serializer.save()

        self.assertEqual(question.text, 'Test Question')
        self.assertEqual(question.survey, survey)
class SurveySerializerAPITestCase(APITestCase):
    def test_survey_serializer(self):
        user = UserProfile.objects.create_user(username='testuser', password='testpassword',email='testuser@example.com')
        survey_data = {'title': 'Test Survey', 'creator': user.id}
        serializer = SurveySerializer(data=survey_data)
        self.assertTrue(serializer.is_valid())
        survey = serializer.save()
        self.assertEqual(survey.title, 'Test Survey')
        self.assertEqual(survey.creator, user)

class AnswerSerializerAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.survey = Survey.objects.create(title='Test Survey', creator=self.user)
        self.question = Question.objects.create(survey=self.survey, text='Test Question')
        self.option = Option.objects.create(question=self.question, text='Test Option')

    def test_answer_serializer(self):
        self.client.force_authenticate(user=self.user)

        answer_data = {'question': self.question.id, 'option': self.option.id}
        response = self.client.post('/answers/', answer_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_answer_submission_invalid_question(self):
        self.client.force_authenticate(user=self.user)

        invalid_question_id = 999999
        answer_data = {'question': invalid_question_id, 'option': self.option.id}
        response = self.client.post('/answers/', answer_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("question", response.data)

    def test_answer_submission_invalid_option(self):
        self.client.force_authenticate(user=self.user)

        invalid_option_id = 999999
        answer_data = {'question': self.question.id, 'option': invalid_option_id}
        response = self.client.post('/answers/', answer_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("option", response.data)

    def test_answer_submission_missing_question(self):
        self.client.force_authenticate(user=self.user)

        answer_data = {'option': self.option.id}
        response = self.client.post('/answers/', answer_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("question", response.data)

    def test_answer_submission_missing_option(self):
        self.client.force_authenticate(user=self.user)

        answer_data = {'question': self.question.id}
        response = self.client.post('/answers/', answer_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("option", response.data)
