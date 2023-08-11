from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Answer, Survey, Question, Option


admin.site.register(Answer)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)



