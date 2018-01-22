from django.db import models
from django.core.urlresolvers import reverse
from django.forms import ModelForm, forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Count


trans_Choices = (
    ('B','Bus'), ('T','Train'), ('P','Plane'), ('S','Ship')
)

residence_Choices = (
    ('M', 'Motel'), ('T', '3 star Hotel'), ('F', '4 star Hotel'), ('V', '5 star Hotel'), ('N', 'N/N')
)

class Trip(models.Model):
    name = models.CharField(max_length=250)

    origin = models.CharField(max_length=50, default="Cairo")
    destination = models.CharField(max_length=50)

    departing_date = models.DateField()
    returning_date = models.DateField()

    transportstion = models.CharField(max_length=10, choices= trans_Choices)
    residence = models.CharField(max_length=20, choices= residence_Choices)

    price = models.PositiveSmallIntegerField()

    capacity = models.PositiveSmallIntegerField(default=0)

    reservation = models.ManyToManyField(User)


    def get_absolute_url(self):
        return reverse('trips:detial', kwargs={'pk': self.pk})

    def get_no_of_reservation(self):
        return User.objects.filter(pk = self.pk).count()

    def __str__(self):
        return self.name


class Question(models.Model):
    Q_content = models.CharField(max_length=500)
    Q_trip = models.ForeignKey(Trip, related_name='question', on_delete= models.CASCADE)
    asked_by = models.ForeignKey(User, related_name='question', on_delete= models.CASCADE)
    asked_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.Q_content
