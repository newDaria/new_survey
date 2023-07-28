

from django.apps import AppConfig

class SurveyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'survey_app'

    def ready(self):
        import survey_app.signals
        from . import cron
