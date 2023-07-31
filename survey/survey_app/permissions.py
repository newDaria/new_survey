from rest_framework.permissions import BasePermission
from .models import Survey

class CanUpdateSurveyPermission(BasePermission):
    def has_permission(self, request, view):
        survey_id = view.kwargs.get('survey_id')
        survey = Survey.objects.get(pk=survey_id)

        # Check if the current user is the creator of the survey
        return request.user == survey.creator
