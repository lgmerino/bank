from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class BankUser(models.Model):
    """
    Model for users
    first_name, last_name and iban are required
    """
    first_name = models.CharField(max_length=30, blank=False, verbose_name=_('First name'))
    last_name = models.CharField(max_length=30, blank=False, verbose_name=_('Last name'))
    iban = models.CharField(max_length=34, blank=False, verbose_name=_('IBAN'), unique=True)
    administrator = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _(u'Bank user')
        verbose_name_plural = _(u'Bank users')
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.iban)
