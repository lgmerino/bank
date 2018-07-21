from django import forms

from .models import BankUser


class BankUserUpdateForm(forms.ModelForm):
    class Meta:
        model = BankUser
        fields = ('first_name',
                  'last_name',
                  'iban',)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        return first_name.upper().strip()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        return last_name.upper().strip()

    def clean_iban(self):
        iban = self.cleaned_data.get('iban', '')
        return iban.upper().strip()


class BankUserCreateForm(BankUserUpdateForm):
    pass


class BankUserDeleteForm(forms.ModelForm):
    pass
