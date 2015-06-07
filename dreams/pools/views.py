from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
from models import Dreams, User


# # def index(request):
# #     latest_users_list = User.objects.order_by('-registration_date')[:3]
# #     template = loader.get_template('pools/index.html')
# #     context = RequestContext(request, {
# #         'latest_users_list' : latest_users_list,
# #     })
# #     return HttpResponse(template.render(context))
#
# def index(request):
#     latest_users_list = User.objects.order_by('-registration_date')[:3]
#     context = {'latest_users_list' : latest_users_list,}
#     return render(request, 'pools/index.html', context)
#
# # def detail_dream(request, dream_id):
# #     try:
# #         dream = Dreams.objects.get(id=dream_id)
# #     except Dreams.DoesNotExist:
# #         raise Http404('Dream not exist')
# #     return render(request, 'pools/dreams.html', {'dream' : dream})
#
# def detail_dream(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     return render(request, 'pools/dreams.html', {'user' : user})
#
# def detail_user(request, user_id):
#     response = "You're looking at the results of user_id %s."
#     return HttpResponse(response % user_id)
#
# def delete_dream(request, user_id):
#     p = get_object_or_404(User, pk=user_id)
#     try:
#         selected_dream = p.dreams_set.get(pk=request.POST['dream'])
#     except (KeyError, Dreams.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'pools/dreams.html', {
#             'user': p,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#
#         # selected_dream.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('pools:results', args=(p.id,)))



class IndexView(generic.ListView):
    template_name = 'pools/index.html'
    context_object_name = 'latest_users_list'

    def get_queryset(self):
        return User.objects.order_by('-registration_date')[:3]


class DetailView(generic.DetailView):
    model = User
    template_name = 'pools/dreams.html'


class ResultsView(generic.DetailView):
    model = Dreams
    template_name = 'pools/dreams.html'


def vote(request, question_id):
    # same as above
    pass

