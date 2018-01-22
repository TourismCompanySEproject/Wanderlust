from django.conf.urls import url
from . import views

app_name = 'trips'

urlpatterns = [
    # /
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /<trip-id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /signup
    url(r'^signup/$', views.signup, name='signup')
]
