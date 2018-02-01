from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Trip, Question, Reservation
from .forms import SignUpForm, NewQuestionForm, ReservationForm, PaymentForm, ContactForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from .filters import TripFilter
from django_filters.views import FilterView
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError


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
            question = Question()
            question.Q_content = request.POST.get('c')
            question.Q_trip = trip
            question.asked_by = request.user
            question.save()

            return redirect(reverse('trips:detail', kwargs={'pk':pk}))
    return render(request, 'registration/login.html')


def reply_question(request, pk, question_pk):
    if request.user.is_staff:
        question = get_object_or_404(Question, Q_trip__pk=pk, pk=question_pk)
        trip = get_object_or_404(Trip ,pk=pk)
        if request.method == 'POST':
            re_question = Question()
            re_question.Q_content = request.POST.get('c')
            re_question.Q_trip = trip
            re_question.reply_to = question_pk
            re_question.asked_by = request.user
            re_question.save()

            return redirect(reverse('trips:detail', kwargs={'pk': pk}))
    return render(request, 'registration/login.html')

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
            return redirect('trips:login')
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
            'adult_price' ,'capacity']

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
def Booking(request,pk):

    book = ReservationForm()
    book.trip = get_object_or_404(Trip ,pk=pk)
    book.customer = request.user
    book.number = request.GET.get('n')

    return render_to_response("trips/booking-form.html")

class ReservationView(View):

    def post(self, request, pk):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.trip = get_object_or_404(Trip, pk=pk)
            reservation.customer = request.user
            reservation.save()

            return redirect('trips:detail' , pk)
        return render(request, 'trips/booking-form.html', {'form': form})


    def get(self, request, pk):
        form = ReservationForm()
        form.trip = get_object_or_404(Trip, pk=pk)
        form.customer = request.user

        return render(request, 'trips/booking-form.html', {'form': form})

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
        reservations = Reservation.objects.all()
        query = request.GET.get("q")
        if query:
            return render(request, 'trips/admin-panel.html',
                          {'trips' : trips.objects.filter(
                            Q(name__icontains=query) |
                            Q(destination__icontains=query)
                            )}
                          )

        else:
            return render(request,
                          'trips/admin-panel.html',
                          {'trips' : trips, 'questions':questions,
                           'reservations': reservations })


#
# @method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'registration/update_my_account.html'
    fields = ('first_name', 'last_name', 'email',)
    success_url = reverse_lazy('trips:my_account')

    def get_object(self):
        return self.request.user

class UserView(generic.ListView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/my_account.html'


def contact(request):
    subject = request.POST.get('topic', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['Wanderlust.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return render(request, 'trips/thankyou.html')
    else:
        return render(request, 'trips/contact.html', {'form': ContactForm()})

    return render(request, 'trips/contact.html', {'form': ContactForm()})


def thankyou(request):
    return render_to_response('trips:thankyou')

def subscribe(request):
    email = request.POST.get('e')

    if email:
        try:
            send_mail('Newsletter', 'Newsletter test','Wanderlust.com' ,[email] )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect(reverse('trips:index'))
    else:
        return redirect(reverse('trips:index'))
