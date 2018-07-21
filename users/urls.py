from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bank_user/$',
        views.BankUserListView.as_view(),
        name='BankUserListView'),
    url(r'^bank_user/(?P<pk>[0-9]+)/$',
        views.BankUserDetailView.as_view(),
        name='BankUserDetailView'),
    url(r'^bank_user/create/$',
        views.BankUserCreateView.as_view(),
        name='BankUserCreateView'),
    url(r'^bank_user/update/(?P<pk>[0-9]+)/$',
        views.BankUserUpdateView.as_view(),
        name='BankUserUpdateView'),
    url(r'^bank_user/delete/(?P<pk>[0-9]+)/$',
        views.BankUserDeleteView.as_view(),
        name='BankUserDeleteView'),
]
