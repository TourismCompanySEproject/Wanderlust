from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django_filters.views import FilterView

app_name = 'trips'

urlpatterns = [
    # Home page
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /<trip-id>/
    url(r'^trip/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
     # trip//<trip-id>/question/
    url(r'^trip/(?P<pk>[0-9]+)/question/$', views.newQuestion, name='new_question'),
    # /trip/<trip-id>/question/<question-id>/reply/
    url(r'^trip/(?P<pk>[0-9]+)/question/(?P<question_pk>[0-9]+)/reply/$', views.reply_question, name='reply_question'),
    # /signup
    url(r'^signup/$', views.signup, name='signup'),
    # /login
    url(r'^login/$', auth_views.login , name='login'),
    # /logout
    url(r'^logout/$', auth_views.logout ,{'next_page': 'trips:index' }, name='logout'),

    # Admin panel
    url(r'^admin_panel/$', views.admin_panel, name='admin_panel'),
    # /trip/add/
    url(r'^create_trip/$', views.TripCreate.as_view(), name='create_trip'),
    # /trip/2/
    url(r'^trip/(?P<pk>[0-9]+)/edit/$', views.TripUpdate.as_view(), name='trip-update'),
    # delete
    url(r'^trip/(?P<pk>[0-9]+)/delete_album/$', views.TripDelete.as_view(), name='delete_trip'),

    # filter
    url(r'^filter/$', views.TripFilterView.as_view(), name='filter'),




]
