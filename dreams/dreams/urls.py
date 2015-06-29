from django.conf.urls import patterns, include, url
from registration.forms import RegistrationFormUniqueEmail
from registration.views import RegistrationView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dreams.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^pools/', include('pools.urls', namespace='pools')),
                       url(r'^users/', include('users.urls', namespace='users')),
                       url(r'^accounts/register/', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
                       url(r'^accounts/', include('registration.backends.default.urls')),
)
