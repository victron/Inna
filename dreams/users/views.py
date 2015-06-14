from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Dreams
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import

def logining(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('users:home', args=(form.get_user_id(),)))
        else:
            return  HttpResponseRedirect(reverse('users:login'))
    else:
        form = AuthenticationForm()
    return render(request, 'users/logining.html', {'form' : form})


def home(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('users:login'))
    return render(request, 'users/home.html', {'user' : request.user})


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        data = request.POST.copy()
        # errors = form.clean_password2()
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('users:login'))
    return render(request, 'users/registration.html', {'form' : form})


def my_dreams(request):
    pass


class DreamsView(generic.ListView):
    model = Dreams
    # queryset = Dreams.objects.filter(user__id=2)
    template_name = 'users/dreams.html'
    context_object_name = 'all_dreams'

    def get_queryset(self):
        return Dreams.objects.filter(user__id=self.request.user.id).order_by('-dream_date')[:5]


class DreamDetails(generic.DetailView):
    model = Dreams
    template_name = 'users/dream.html'
    context_object_name = 'dream_details'





