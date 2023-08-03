from rest_framework import serializers
from .models import Survey, Question, Option, Answer
from django.contrib.auth.models import User
from django.utils import timezone


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    text = serializers.CharField(required=False)
    # Add the following line to make the 'survey' field required
    survey = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), write_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {'text': {'required': False}}



class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # or StringRelatedField

    class Meta:
        model = Survey
        fields = ['id', 'title', 'questions','creator']
#
# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = '__all__'
#
#     def create(self, validated_data):
#         question = validated_data['question']
#         option = validated_data['option']
#
#         answer = Answer.objects.create(question=question, option=option)
#         return answer



class AnswerSerializer(serializers.ModelSerializer):
    # Add the 'required=True' parameter to the 'question' field
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=True)
    option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all())

    class Meta:
        model = Answer
        fields = ['question', 'option']

    def create(self, validated_data):
        user = self.context['request'].user
        if user:
            # Get the current date
            today = timezone.now().date()

            # Count the number of answers submitted by the user on the current date
            user_submission_count = Answer.objects.user_submission_count_for_day(user, today)
            print(user_submission_count)


            if user_submission_count >= 5:
                print("You have already submitted the maximum allowed answers for today.")
                raise serializers.ValidationError("You have already submitted the maximum allowed answers for today.")


        question = validated_data['question']
        option = validated_data['option']

        answer = Answer.objects.create(question=question, option=option, creator=user)
        return answer
