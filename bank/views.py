from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy


class LogoutView(RedirectView):
    url = reverse_lazy('social:disconnect', args=['google-oauth2'])
