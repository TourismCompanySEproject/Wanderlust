from django.conf.urls import url
from . import views

app_name = 'trips'

urlpatterns = [
    # /trips/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /trips/<trip-id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
