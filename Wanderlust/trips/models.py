from django.db import models
from django.core.urlresolvers import reverse
from django.forms import ModelForm


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

    def get_absolute_url(self):
        return reverse('trips:detial', kwargs={'pk': self.pk})


    def __str__(self):
        return self.name