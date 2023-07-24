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

    def create(self, validated_data):
        question_id = validated_data['question']['id']
        option_id = validated_data['option']['id']

        # Retrieve the related Question and Option objects
        question = Question.objects.get(id=question_id)
        option = Option.objects.get(id=option_id)

        # Create the Answer object with the correct question and option
        answer = Answer.objects.create(question=question, option=option)
        return answer
