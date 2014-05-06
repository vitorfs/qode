from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'quiz.views.home', name='home'),
    url(r'^login/$', 'auth.views.login', name='login'),
    url(r'^facebook/$', 'auth.views.facebook', name='facebook'),
)
