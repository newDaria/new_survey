from rest_framework import serializers
from .models import Survey, Question, Option, Answer
from django.contrib.auth.models import User


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
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # or StringRelatedField

    class Meta:
        model = Survey
        fields = ['id', 'title', 'questions','creator']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    class AnswerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Answer
            fields = '__all__'

        def create(self, validated_data):
            question = validated_data['question']
            option = validated_data['option']

            answer = Answer.objects.create(question=question, option=option)
            return answer

