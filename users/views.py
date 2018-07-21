from django.views.generic import DeleteView, CreateView, UpdateView, DetailView, TemplateView, RedirectView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext as _
from braces.views import LoginRequiredMixin
from django_tables2 import SingleTableView

from .models import BankUser
from . import forms
from . import tables


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.url = reverse('BankUserListView')
        else:
            self.url = reverse('social:begin', args=['google-oauth2'])

        return super().get_redirect_url(*args, **kwargs)


class BankUserListView(LoginRequiredMixin, SingleTableView):
    template_name = 'bank_user/list.html'
    model = BankUser
    table_class = tables.BankUserListTable


class BankUserCreateView(LoginRequiredMixin, CreateView):
    model = BankUser
    form_class = forms.BankUserCreateForm
    template_name = 'bank_user/create.html'
    success_url = reverse_lazy('BankUserListView')

    def form_valid(self, form):
        # we need to add the administrator
        self.object = form.save(commit=False)
        self.object.administrator = self.request.user
        self.object.save()

        # success message
        message = _('New user {0} {1} created'.format(self.object.first_name,
                                                      self.object.last_name))
        messages.success(self.request, message)

        return HttpResponseRedirect(self.get_success_url())


class BankUserUpdateView(LoginRequiredMixin, UpdateView):
    model = BankUser
    form_class = forms.BankUserUpdateForm
    template_name = 'bank_user/update.html'

    def get_success_url(self):
        # success message
        message = _('User {0} {1} updated'.format(self.object.first_name,
                                                  self.object.last_name))
        messages.success(self.request, message)

        return reverse('BankUserListView')


class BankUserDeleteView(LoginRequiredMixin, DeleteView):
    model = BankUser
    form_class = forms.BankUserDeleteForm
    template_name = 'bank_user/delete.html'
    success_url = reverse_lazy('BankUserListView')

    def delete(self, request, *args, **kwargs):
        # success message
        bank_user = self.get_object()
        message = _('User {0} {1} updated'.format(bank_user.first_name,
                                                  bank_user.last_name))

        response = super().delete(request, *args, **kwargs)

        messages.success(self.request, message)

        return response


class BankUserDetailView(LoginRequiredMixin, DetailView):
    model = BankUser
    template_name = 'bank_user/detail.html'
