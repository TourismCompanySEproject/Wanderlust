from django.shortcuts import render, redirect
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from .models import AdminUser
from django.contrib.auth import login as auth_login
from trips.models import Trip

class IndexView(generic.ListView):
    template_name = 'administrator/index.html'
    context_object_name = 'all_trips'

    def get_queryset(self):
        return Trip.objects.all()

class DetailView(generic.DetailView):
    model = Trip
    template_name = 'administrator/detail.html'

def signup(request):
    if request.method=='POST':

        form= AdminUser(request.POST)
        if form.is_valid():
            user= form.save()
            auth_login(request, user)
            return redirect('administrator:index')
    else:
        form = AdminUser()
    return  render(request, 'administrator/signup.html', {'form':form})

def auth_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_admin:
                if user.is_active:
                    auth_login(request, user)
                    return render(request, 'administrator/index.html')
                else:
                    return render(request, 'administrator/login.html', {'error_message': 'Your account has been disabled'})
            else: return render(request, 'administrator/login.html', {'error_message': 'Your account is not admin'})
        else:
            return render(request, 'administrator/login.html', {'error_message': 'Invalid login'})
    return render(request, 'administrator/login.html')

