from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Response, Survey, Question, Option


admin.site.register(Response)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)



