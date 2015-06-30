__author__ = 'vic'


from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from . import views


urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^home/$', views.home, name='home'),
    url(r'^', include('django.contrib.auth.urls')),
    # url(r'^registration/$', views.register, name='register'),

    url(r'^dreams/$', views.DreamsView.as_view(), name='dreams'),
    url(r'^NewDream/$', views.CreateDreamtView.as_view(), name='create_dream'),
    url(r'^(?P<pk>[0-9]+)/dream$', views.DreamDetails.as_view(), name='dream_details'),
    url(r'^(?P<pk>[0-9]+)/update_dream', views.UpdateDreamtView.as_view(), name='update_dream'),
    url(r'^(?P<pk>[0-9]+)/delete_dream$', views.DeleteDreamView.as_view(), name='delete_dream'),

]

