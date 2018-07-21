from django import forms

from .models import BankUser


class BankUserUpdateForm(forms.ModelForm):
    class Meta:
        model = BankUser
        fields = ('first_name',
                  'last_name',
                  'iban',)


class BankUserCreateForm(BankUserUpdateForm):
    pass


class BankUserDeleteForm(forms.ModelForm):
    pass
