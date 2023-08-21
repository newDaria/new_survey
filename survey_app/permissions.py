
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from survey_app.models import Survey
from rest_framework.exceptions import PermissionDenied


class CanUpdateSurveyPermission(BasePermission):
    def has_permission(self, request, view):
        survey_id = view.kwargs.get('survey_id')
        try:
            survey = get_object_or_404(Survey, pk=survey_id)
        except Survey.DoesNotExist:
            # If the Survey object does not exist, return False to deny permission
            return False

        # Check if the current user is the creator of the survey
        if request.user == survey.creator:
            return True

        # Raise PermissionDenied if the user is not the creator
        raise PermissionDenied("You do not have permission to update this survey.")
