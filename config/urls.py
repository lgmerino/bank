from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'bank.views.home', name='home'),
    # url(r'^bank/', include('bank.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^', include('users.urls')),
]
