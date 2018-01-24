from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

app_name = 'trips'

urlpatterns = [
    # /
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /<trip-id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /signup
    url(r'^signup/$', views.signup, name='signup'),
    # /login
#    url(r'^login/$', auth_views.login , name='login'),
    # /logout
#    url(r'^logout/$', auth_views.logout ,{'next_page': '/' }, name='logout'),
    # /admin
#    url(r'^admin/$', admin.site.urls),

    # /login
    url(r'^login/$', views.UserFormView , name='login'),


]
