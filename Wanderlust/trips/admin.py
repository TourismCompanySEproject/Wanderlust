from django.contrib import admin
from .models import Trip,Question, Reservation
from .forms import User

admin.site.register(Trip)
admin.site.register(Question)
admin.site.register(Reservation)