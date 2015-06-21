from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dreams.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^pools/', include('pools.urls', namespace='pools')),
                       url(r'^users/', include('users.urls', namespace='users')),
                       url(r'^accounts/', include('registration.backends.default.urls')),
)
