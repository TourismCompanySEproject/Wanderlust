from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Trip
from .forms import SignUpForm

class IndexView(generic.ListView):
    template_name = 'trips/index.html'
    context_object_name = 'all_trips'

    def get_queryset(self):
        return Trip.objects.all()

class DetailView(generic.DetailView):
    model = Trip
    template_name = 'trips/detail.html'



def signup(request):
    if request.method=='POST':

        form= SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            auth_login(request, user)
            return redirect('trips:index')
    else:
        form = SignUpForm()
    return  render(request, 'trips/signup.html', {'form':form})
