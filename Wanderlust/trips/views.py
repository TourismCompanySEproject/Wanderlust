from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Trip, Question
from .forms import SignUpForm, NewQuestionForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .filters import TripFilter
from django_filters.views import FilterView
from .filters import TripFilter
from django.http import HttpResponse

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

@login_required(redirect_field_name='trips/new-question.html', login_url='trips:login')
def newQuestion(request, pk):
    if request.user.is_authenticated:
        trip = get_object_or_404(Trip, pk=pk)
        if request.method == 'POST':
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.Q_trip = trip
                question.asked_by = request.user
                question.save()

                return redirect(reverse('trips:detail', kwargs={'pk':pk}))
        else:
            form = NewQuestionForm()
        return render(request, 'trips/new-question.html', {'form': form})
    return render(request, 'registration/login.html')


def reply_question(request, pk, question_pk):
    if request.user.is_staff:
        question = get_object_or_404(Question, Q_trip__pk=pk, pk=question_pk)
        if request.method == 'POST':
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.Q_trip = trip
                question.asked_by = request.user
                question.save()

                trip_url = reverse('trips:detail', kwargs={'pk': pk, 'question_pk': question_pk})

                return redirect(trip_url)
        else:
            form = NewQuestionForm()
        return render(request, 'trips/new-question.html', {'form': form})

# class NewQuestionView(CreateView):
#     model = Question
#     form_class = NewQuestionForm
#     success_url = reverse_lazy('trips:detail')
#     template_name = 'new-question.html'

# class NewQuestionView(View):
#
#     def post(self, request):
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('trips:detail')
#         return render(request, 'new-question.html', {'form': form})
#
#
#     def get(self, request):
#         form = QuestionForm()
#         return render(request, 'new-question.html', {'form': form})

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
                return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    return render(request, 'registration/login.html')


class TripCreate(CreateView):
    model = Trip
    fields = ['name','description',
              'origin', 'destination',
            'departing_date', 'returning_date',
            'transportstion', 'residence',
            'adult_price' ,'kid_price', 'capacity']


class TripUpdate(UpdateView):
    model = Trip
    fields = ['name', 'origin','description','destination',
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

def admin_panel(request):
    if not request.user.is_authenticated:
        return redirect('trips:login')
    if not request.user.is_staff:
        return HttpResponse("<h3> You are not Authorized to view this page.</h3>"
                            "<br>"
                            "<a href=/Wanderlust/>return home</a>"
                            )
    else:
        trips = Trip.objects.all()
        questions = Question.objects.all()
        query = request.GET.get("q")
        if query:
            return render(request, 'trips/admin-panel.html',
                          {'trips' : trips.objects.filter(
                            Q(name__icontains=query) |
                            Q(destination__icontains=query)
                            )}
                          )

        else:
            return render(request, 'trips/admin-panel.html', {'trips' : trips, 'questions':questions })