from survey_app.models import Survey, Question, Option, Answer
from survey_app.models import UserProfile
from rest_framework.test import APITestCase
from survey_app.factories import SurveyFactory, QuestionFactory, OptionFactory, AnswerFactory,UserProfileFactory

class ModelTests(APITestCase):
    def setUp(self):
        self.user = UserProfileFactory()
        self.survey = SurveyFactory(creator=self.user)
        self.question = QuestionFactory(survey=self.survey)
        self.option = OptionFactory(question=self.question)
        self.answer = AnswerFactory(question=self.question, option=self.option, creator=self.user)

    def test_survey_model(self):
        self.assertEqual(self.survey.title, 'Test Survey')
        self.assertEqual(self.survey.creator, self.user)

    def test_question_model(self):
        self.assertEqual(self.question.text, 'Test Question')
        self.assertEqual(self.question.survey, self.survey)

    def test_option_model(self):
        self.assertEqual(self.option.text, 'Test Option')
        self.assertEqual(self.option.question, self.question)

    def test_answer_model(self):
        self.assertEqual(self.answer.question, self.question)
        self.assertEqual(self.answer.option, self.option)
        self.assertEqual(self.answer.creator, self.user)
