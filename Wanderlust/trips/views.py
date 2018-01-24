from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Trip
from .forms import SignUpForm, LogInForm
from django.views.generic import View

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



class TripCreate(CreateView):
    model = Trip
    fields = ['name', 'origin', 'destination',
            'departing_date', 'returning_date',
            'transportstion', 'residence',
            'price' ,'capacity']


class TripUpdate(UpdateView):
    model = Trip
    fields = ['name', 'origin', 'destination',
            'departing_date', 'returning_date',
            'transportstion', 'residence',
            'price' ,'capacity']

class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trips:index')


class UserFormView(View):
    form_class = LogInForm
    template_name = 'registeration/login.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    #process form data
    def post(self, request):
        form =  self.form_class(request.POST)

        if form.is_valid():
            #returns User objects if credentials are correct
            user = authenticate(username= username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('trips:index')

        return render(request, self.template_name, {'form': form})