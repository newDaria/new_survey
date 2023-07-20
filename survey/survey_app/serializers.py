from rest_framework import serializers
from .models import Survey, Question, Option, Answer


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    text = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = '__all__'
        # Add the following line to allow partial updates
        extra_kwargs = {'text': {'required': False}}


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
