from django.conf.urls import include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'bank.views.home', name='home'),
    # url(r'^bank/', include('bank.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('users.urls')),
]
