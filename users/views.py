from django.views.generic import DeleteView, CreateView, UpdateView, DetailView, TemplateView, RedirectView
from django.core.urlresolvers import reverse

from .models import BankUser
from . import forms


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.url = reverse('BankUserListView')
        else:
            self.url = reverse('social:begin', args=['google-oauth2'])

        return super().get_redirect_url(*args, **kwargs)


class BankUserListView(TemplateView):
    template_name = 'bank_user/list.html'


class BankUserCreateView(CreateView):
    model = BankUser
    form_class = forms.BankUserCreateForm
    template_name = 'bank_user/create.html'


class BankUserUpdateView(UpdateView):
    model = BankUser
    form_class = forms.BankUserUpdateForm
    template_name = 'bank_user/update.html'


class BankUserDeleteView(DeleteView):
    model = BankUser
    form_class = forms.BankUserDeleteForm
    template_name = 'bank_user/delete.html'


class BankUserDetailView(DetailView):
    model = BankUser
    template_name = 'bank_user/detail.html'
