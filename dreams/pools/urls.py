__author__ = 'vic'

from django.conf.urls import url

from . import views

# urlpatterns = [
#     # ex: /polls/
#     url(r'^$', views.index, name='index'),
#     # ex: /polls/5/
#     url(r'^(?P<user_id>[0-9]+)/$', views.detail_dream, name='detail'),
#     # ex: /polls/5/results/
#     url(r'^(?P<user_id>[0-9]+)/user/$', views.detail_user, name='results'),
#     # ex: /polls/5/delete/
#     url(r'^(?P<user_id>[0-9]+)/dream/$', views.delete_dream, name='delete'),
# ]

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]