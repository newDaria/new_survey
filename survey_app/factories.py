import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from survey_app.models import UserProfile, Survey, Question, Option, Answer

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.Sequence(lambda n: f'user{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False


class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Survey

    title = 'Test Survey'  # Set the title explicitly
    creator = factory.SubFactory(UserProfileFactory)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    survey = factory.SubFactory(SurveyFactory)
    text = 'Test Question'  # Set the text explicitly


class OptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Option

    question = factory.SubFactory(QuestionFactory)
    text = 'Test Option'  # Set the text explicitly


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    option = factory.SubFactory(OptionFactory)
    creator = factory.SubFactory(UserProfileFactory)
    created_at = factory.Faker('date_time_this_year', tzinfo=timezone.get_current_timezone())
