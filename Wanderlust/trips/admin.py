from django.contrib import admin
from .models import Trip,Question
from .forms import User

admin.site.register(Trip)
admin.site.register(Question)