from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Survey, Question, Option, Answer
from .serializers import SurveySerializer, QuestionSerializer, OptionSerializer, AnswerSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SurveyCreateView(generics.CreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        # Set the creator field to the current user (assuming you have access to the user object)
        serializer.save(creator=self.request.user)


class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        survey_data = serializer.data
        survey_id = survey_data['id']

        # Get all questions related to the survey using the reverse relationship name 'questions'
        questions = Question.objects.filter(survey_id=survey_id)
        question_serializer = QuestionSerializer(questions, many=True)
        survey_data['questions'] = question_serializer.data


        return Response(survey_data)

# to create a list with all survey titles
class SurveyListView(generics.ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = 'pk'

class QuestionUpdateView(generics.UpdateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'pk'

class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        survey_id = self.kwargs['survey_id']
        survey = Survey.objects.get(pk=survey_id)
        serializer.save(survey=survey)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'pk'

class OptionCreateView(generics.CreateAPIView):
    serializer_class = OptionSerializer

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Option.objects.filter(question_id=question_id)

class OptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    lookup_field = 'pk'

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'question_id'  # Assuming you want to use 'question_id' as the lookup field

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return self.queryset.filter(question__id=question_id)
