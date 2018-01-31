from django.conf.urls import url, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django_filters.views import FilterView
from django.urls import reverse_lazy

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
    # Book
    url(r'^trip/(?P<pk>[0-9]+)/booking/$', views.ReservationView.as_view(), name='book'),

    # user account
    url(r'^account/$', views.UserView.as_view(), name='my_account'),


    # Password reset
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='trips/password_reset.html',
            email_template_name='trips/password_reset_email.html',
            subject_template_name='trips/password_reset_subject.txt'
            ), {'post_reset_redirect': 'trips:password_reset_done'},
        name='password_reset'),
    # Password reser done
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='trips/password_reset_done.html'),
        name='password_reset_done'),
    #Password reset confirm
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='trips/password_reset_confirm.html'),
        name='password_reset_confirm'),
    #Password reset complete
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='trips/password_reset_complete.html'),
        name='password_reset_complete'),

    # update account
    url(r'^settings/account/edit/$', views.UserUpdateView.as_view(), name='update_my_account'),

    #Change password
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url=reverse_lazy('trips:password_change_done')),
        name='password_change'),
    #Password change done
    url(r'^settings/password/done/$',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'),
        name='password_change_done'),

]
