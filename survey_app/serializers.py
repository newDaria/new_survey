from rest_framework import serializers
from .models import Survey, Question, Option, Answer
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    survey = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), write_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'survey', 'options']
        extra_kwargs = {'text': {'required': False}}


User = get_user_model()

def get_request_user(serializer):
    try:
        return serializer.context['request'].user
    except KeyError:
        return None

class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # or StringRelatedField

    class Meta:
        model = Survey
        fields = ['id', 'title', 'questions', 'creator']

    def create(self, validated_data):
        # Set the creator field to the current user
        request_user = get_request_user(self)
        if request_user is not None:
            validated_data['creator'] = request_user
        return super().create(validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    # Add the 'required=True' parameter to the 'question' field
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=True)
    option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all())

    class Meta:
        model = Answer
        fields = ['question', 'option']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            # Get the current date
            today = timezone.now().date()

            # Count the number of answers submitted by the user on the current date
            user_submission_count = Answer.user_submission_count_for_day(user, today)
            print(user_submission_count)


            if user_submission_count >= 5:
                print("You have already submitted the maximum allowed answers for today.")
                raise serializers.ValidationError("You have already submitted the maximum allowed answers for today.")


        question = validated_data['question']
        option = validated_data['option']

        answer = Answer.objects.create(question=question, option=option, creator=user)
        return answer


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
