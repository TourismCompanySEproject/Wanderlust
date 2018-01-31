from django.db import models
from django.forms import ModelForm, forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Count
from datetime import datetime, timezone, date
from django.utils.html import mark_safe
from django.utils.text import Truncator
from markdown import markdown
from django.urls import reverse

trans_Choices = (
    ('B','Bus'), ('T','Train'), ('P','Plane'), ('S','Ship')
)

residence_Choices = (
    ('M', 'Motel'), ('T', '3 star Hotel'), ('F', '4 star Hotel'), ('V', '5 star Hotel'), ('N', 'N/N')
)

class Trip(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=5000, null=True)

    origin = models.CharField(max_length=50, default="Cairo")
    destination = models.CharField(max_length=50)

    departing_date = models.DateField()
    returning_date = models.DateField()

    transportstion = models.CharField(max_length=10, choices=trans_Choices)
    residence = models.CharField(max_length=20, choices=residence_Choices)

    adult_price = models.PositiveSmallIntegerField(default=0)
    kid_price = models.PositiveSmallIntegerField(default=0)

    capacity = models.PositiveSmallIntegerField(default=0)

    trip_image1 = models.FileField(default='', blank=True)
    trip_image2 = models.FileField(default='', blank=True)
    trip_image3 = models.FileField(default='', blank=True)

    def get_absolute_url(self):
        return reverse('trips:detail', kwargs={'pk': self.pk})

    def get_no_of_reservation(self):
        reserv = Reservation.objects.filter(trip=self)
        no = 0
        for res in reserv:
            no += res.number
        return no

    def check_time(self):
        date_today = date.today()
        if  date_today <= self.departing_date :
            return True
        else:
            return False

    def __str__(self):
        return self.name



class Question(models.Model):
    Q_content = models.TextField(max_length=500)
    reply_to = models.PositiveSmallIntegerField(default='0')
    Q_trip = models.ForeignKey(Trip, on_delete= models.CASCADE)
    asked_by = models.ForeignKey(User, related_name='question', on_delete= models.CASCADE)
    asked_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.Q_content


    def get_message_as_markdown(self):
        return mark_safe(markdown(self.Q_content, safe_mode='escape'))

class Reservation(models.Model):
    trip = models.ForeignKey(Trip, on_delete = models.CASCADE)
    customer = models.ForeignKey(User, on_delete= models.CASCADE)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.trip.name