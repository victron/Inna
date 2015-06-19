from django.shortcuts import render
from django import forms
import forms
# Create your views here.
from django.views import generic
from django.contrib.auth import  views
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
# from django.contrib.auth import views as auth_views

from models import Dreams
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import

# def logining(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             if request.POST.get('next'):
#                 return HttpResponseRedirect(request.POST['next'])
#             return HttpResponseRedirect(reverse('users:home', args=(form.get_user_id(),)))
#         else:
#             return  HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/login.html', {'form' : form})

# from standart django.contrib.auth
def login(request):
    template_response = views.login(request)
    # Do something with `template_response`
    return template_response

def logout(request):
    template_response = views.logout(request, template_name='user:welcome',)
    return template_response

@login_required
def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('users:login'))
    return render(request, 'users/home.html', {'user' : request.user})

def welcome(request):
    return render(request, 'users/welcome.html')






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


def create_dream(request):
    pass


####################### classes for login and Checking Ownership

class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class DreamsOwnerMixin(object):

    def get_object(self, queryset=None):
        """Returns the object the view is displaying.

        """

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(
            pk=pk,
            user=self.request.user,
        )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise PermissionDenied

        return obj

###########################################################

class DreamsView(LoggedInMixin, generic.ListView):
    model = Dreams
    # queryset = Dreams.objects.filter(user__id=2)
    template_name = 'users/dreams.html'
    context_object_name = 'all_dreams'
    def get_queryset(self):
        return Dreams.objects.filter(user__id=self.request.user.id).order_by('-dream_date')[:5]

    # working method without LoggedInMixin inhering
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(DreamsView, self).dispatch(*args, **kwargs)


class DreamDetails(LoggedInMixin, DreamsOwnerMixin, generic.DetailView):
    model = Dreams
    template_name = 'users/dream.html'
    context_object_name = 'dream_details'


class CreateDreamtView( generic.CreateView):

    model = Dreams
    template_name = 'users/create_dream.html'
    # form_class = forms.NewDreamForm
    fields = ['dream_subject', 'dream_text', 'dream_date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateDreamtView, self).form_valid(form)






