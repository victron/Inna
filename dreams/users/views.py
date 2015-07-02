from django.shortcuts import render
from django import forms
import forms
from .forms import *
# Create your views here.
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import  views
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
# from django.contrib.auth import views as auth_views

from models import Dreams, Dreams_D_Tags, D_Tags
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

 # below views done by django-registration-redux
# def register(request):
#     form = UserCreationForm()
#     if request.method == 'POST':
#         data = request.POST.copy()
#         # errors = form.clean_password2()
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             return HttpResponseRedirect(reverse('users:login'))
#     return render(request, 'users/registration.html', {'form' : form})
#
# # from standart django.contrib.auth
# def login(request):
#     template_response = views.login(request)
#     # Do something with `template_response`
#     return template_response
#
# def logout(request):
#     template_response = views.logout(request, template_name='user:welcome',)
#     return template_response

@login_required
def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'users/home.html', {'user' : request.user})

def welcome(request):
    return render(request, 'users/welcome.html')


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


class CreateDreamtView(LoggedInMixin, DreamsOwnerMixin, SuccessMessageMixin, generic.CreateView):

    model = Dreams
    template_name = 'users/create_dream.html'
    success_url = reverse_lazy('users:dreams')
    # form_class = forms.NewDreamForm
    success_message = "Dream %(dream_subject)s was created successfully"
    fields = ['dream_subject', 'dream_text']
    # fields = [ 'dream_tag_weight']

    # def get_success_url(self):
    #     return reverse('users:dreams')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateDreamtView, self).form_valid(form)

class CreateDreamtView2( generic.CreateView):

    # model = Dreams
    # form_class = Dreams_D_TagsForm
    form_class = DreamForm
    template_name = 'users/create_dream.html'
    success_url = reverse_lazy('users:dreams')
    # form_class = forms.NewDreamForm
    success_message = "Dream %(dream_subject)s was created successfully"
    # fields = ['dream_subject', 'dream_text']
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        # self.object = None
        # form = self.get_form(form_class)
        # ingredient_form = IngredientFormSet()
        # instruction_form = InstructionFormSet()
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form, dream_form=DreamForm, tag_form=Dreams_D_TagsForm))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.form_valid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        tag = Dreams_D_Tags()
        tag.dream_tag_weight=self.request.POST.get('dream_tag_weight')
        tag.dream_tag_id = D_Tags.objects.get(id=self.request.POST.get('dream_tag_id'))
        self.object = form.save()
        # save dream and then can get dream id from object
        tag.dream_id=self.object
        tag.save()
        return HttpResponseRedirect(self.get_success_url())
        # return super(CreateDreamtView2, self).form_valid(tag)

class UpdateDreamtView(LoggedInMixin, DreamsOwnerMixin, SuccessMessageMixin, generic.UpdateView):

    model = Dreams
    template_name = 'users/update_dream.html'
    success_url = reverse_lazy('users:dreams')
    success_message = "Dream %(dream_subject)s was updated successfully"
    # context_object_name = 'dream_details'
    # form_class = forms.NewDreamForm
    fields = ['dream_subject', 'dream_text']


class DeleteDreamView(LoggedInMixin, DreamsOwnerMixin,  generic.DeleteView):
    model = Dreams
    template_name = 'users/delete_dream.html'
    success_url = reverse_lazy('users:dreams')

    # success_message = "Dream  was deleted successfully"


    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(cleaned_data,
    #                                        dream_subject=self.object.dream_subject)

    def delete(self, request, *args, **kwargs):
        message = 'Dream ' + self.get_object().dream_subject +  ' was deleted successfully!'
        messages.success(self.request, message)
        # messages.success(self.request, self.success_message)
        return super(DeleteDreamView, self).delete(request, *args, **kwargs)

    # def get_object(self):
    #     object = super(DeleteDreamView, self).get_object()
    #
    #     return object
    #
    # def get_queryset(self):
    #     return self.request.




