from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Survey, Question, Option, Answer
from .serializers import SurveySerializer, QuestionSerializer, OptionSerializer, AnswerSerializer
# from .signals import send_survey_creation_email

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        # Set the creator field to the current user (assuming you have access to the user object)
        serializer.save(creator=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class SurveyQuestionsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, survey_pk=None):
        survey = get_object_or_404(Survey, pk=survey_pk)
        serializer = SurveySerializer(survey)
        questions = survey.question_set.all()
        question_serializer = QuestionSerializer(questions, many=True)

        response_data = {
            'survey': serializer.data,
            'questions': question_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class QuestionOptionsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, question_pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        serializer = QuestionSerializer(question)
        options = question.option_set.all()
        options_serializer = OptionSerializer(options, many=True)

        response_data = {
            'question': serializer.data,
            'options': options_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, question_pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        serializer = OptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question=question)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

