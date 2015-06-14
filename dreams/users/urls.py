__author__ = 'vic'


from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from . import views


urlpatterns = [
    url(r'^$', views.logining, name='user'),
    url(r'^login/$', views.logining, name='login'),
    url(r'^registration/$', views.register, name='register'),
    # url(r'home/$', views.home, name='home'),
    url(r'^(?P<user_id>[0-9]+)/home/$', views.home, name='home'),
    url('^register/', CreateView.as_view(
            template_name='users/registration.html',
            form_class=UserCreationForm,
            success_url='/users/'
    )),

    url(r'^dreams/$', views.DreamsView.as_view(), name='dreams'),
    url(r'^(?P<pk>[0-9]+)/dream$', views.DreamDetails.as_view(), name='dream_details'),


]
