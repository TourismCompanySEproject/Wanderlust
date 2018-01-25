from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

app_name = 'administrator'

urlpatterns = [
    # /
    url(r'^$', views.IndexView.as_view(), name='index'),
    # # /<trip-id>/
    # url(r'^trip/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /signup
     url(r'^signup/$', views.signup, name='signup'),
    # /login
     url(r'^login/$', auth_views.login , name='login'),
    # # /logout
     url(r'^logout/$', auth_views.logout ,{'next_page': 'administrator:index' }, name='logout'),

    # # /trip/add/
    # url(r'^create_trip/$', views.TripCreate.as_view(), name='create_trip'),
    # # /trip/2/
    # url(r'^trip/(?P<pk>[0-9]+)/$', views.TripUpdate.as_view(), name='album-trip'),
    #
    # url(r'^trip/(?P<pk>[0-9]+)/delete_album/$', views.TripDelete.as_view(), name='delete_trip'),

]
