from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Survey, Question, Option, Answer
from .serializers import SurveySerializer, QuestionSerializer, OptionSerializer, AnswerSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Survey
from .serializers import SurveySerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication



class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    #
    # def perform_create(self, serializer):
    #     # Set the creator field to the current user (assuming you have access to the user object)
    #     serializer.save(creator=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        # Manually call the serializer's create method with the creator set as the request's user
        serializer.save(creator=self.request.user)
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


# class UpdateSurveyAPIView(UpdateAPIView):
#     serializer_class = SurveySerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Survey.objects.all()
#
#     def get_object(self):
#         queryset = self.get_queryset()
#         survey = get_object_or_404(queryset, pk=self.kwargs.get('survey_id'))
#
#         # Check if the current user is the creator of the survey
#         if self.request.user != survey.creator:
#             raise PermissionDenied("You do not have permission to update this survey.")
#
#         return survey

from .permissions import CanUpdateSurveyPermission
class UpdateSurveyAPIView(UpdateAPIView):
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated, CanUpdateSurveyPermission]

    def get_queryset(self):
        return Survey.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        survey = get_object_or_404(queryset, pk=self.kwargs.get('survey_id'))
        self.check_object_permissions(self.request, survey)  # Check permissions
        return survey


class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Print validation errors to the console
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.FILES.get('avatar'):
            self.object.avatar = self.request.FILES['avatar']
            self.object.save()
        return response

# class LoginAPIView(APIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key})
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Print statements to debug
            print(f"Received username: {username}")
            print(f"Received password: {password}")

            user = authenticate(username=username, password=password)
            if user:
                print(f"User authenticated: {user.username}")

                token, created = Token.objects.get_or_create(user=user)

                # Print statement to check token creation
                print(f"Token created: {token.key}")

                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)




