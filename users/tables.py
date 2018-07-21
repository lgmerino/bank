import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _

from . import models


class BankUserListTable(tables.Table):

    options = tables.TemplateColumn(
        template_name='bank_user/column_options_list_view.html',
        orderable=False,
        verbose_name=_('Options'))

    class Meta:
        model = models.BankUser
        per_page = 20
        attrs = {"class": "table"}
        fields = ('first_name',
                  'last_name',
                  'iban',)
