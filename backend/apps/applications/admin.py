from django.contrib import admin
from .models import Application, Assignment
admin.site.register([Application, Assignment])
