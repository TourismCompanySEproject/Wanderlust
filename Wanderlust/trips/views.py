from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Trip


class IndexView(generic.ListView):
    template_name = 'trips/index.html'
    context_object_name = 'all_trips'

    def get_queryset(self):
        return Trip.objects.all()

class DetailView(generic.DetailView):
    model = Trip
    template_name = 'trips/detail.html'
