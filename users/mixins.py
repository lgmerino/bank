from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin


class OnlyAdministratorAllowedMixin(LoginRequiredMixin):
    def get_object(self, queryset=None):
        object = super().get_object()
        if object.administrator == self.request.user:
            return object
        raise PermissionDenied
