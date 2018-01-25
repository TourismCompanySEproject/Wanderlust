from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Trip
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .filters import TripFilter
from django_filters.views import FilterView
from .filters import TripFilter


class IndexView(generic.ListView):
    template_name = 'trips/index.html'
    context_object_name = 'all_trips'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Trip.objects.filter(
                Q(name__icontains=query) |
                Q(destination__icontains=query)
            )

        else:
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

def auth_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'trips/index.html')
            else:
                return render(request, 'trips/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'trips/login.html', {'error_message': 'Invalid login'})
    return render(request, 'trips/login.html')


class TripCreate(CreateView):
    model = Trip
    fields = ['name', 'origin', 'destination',
            'departing_date', 'returning_date',
            'transportstion', 'residence',
            'adult_price' ,'kid_price', 'capacity']


class TripUpdate(UpdateView):
    model = Trip
    fields = ['name', 'origin', 'destination',
            'departing_date', 'returning_date',
            'transportstion', 'residence',
            'adult_price' ,'kid_price' ,'capacity']

class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trips:index')

class TripFilterView(FilterView):
    filterset_class = TripFilter
    template_name= 'trips/filter.html'


#
# @login_required
# def Booking_page(request):
#     return render_to_response("trips:booking-form.html")

@permission_required('entity.can_delete', login_url='trips:login')
def Booking(request):
    return render_to_response("trips/booking-form.html")