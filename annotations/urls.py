from django.conf.urls import patterns, url
from annotations import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^/(?P<id>\d+)/', views.update, name='update')
 )
