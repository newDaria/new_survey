from rest_framework import generics
from .models import Survey, Question, Option, Response
from .serializers import SurveySerializer, QuestionSerializer, OptionSerializer, ResponseSerializer


class SurveyList(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class OptionList(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class ResponseList(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class ResponseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

