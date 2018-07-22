from django.test import TestCase
from django.contrib.auth.models import User

from users.forms import BankUserUpdateForm
from users.models import BankUser



class BankUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='adm1', email='adm1@gmail.com', password='adm1')

    def test_valid_form(self):
        data = {'first_name': 'FirstName1',
                'last_name': 'LastName1',
                'iban': 'IE29AIBK93115212345678'}
        form = BankUserUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'first_name': '',
                'last_name': 'LastName2',
                'iban': 'IL620108000000099999999'}
        form = BankUserUpdateForm(data=data)
        form.is_valid()
        self.assertFalse(form.is_valid())

        data = {'first_name': 'FirstName2',
                'last_name': '',
                'iban': 'IL620108000000099999999'}
        form = BankUserUpdateForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'first_name': 'FirstName2',
                'last_name': 'LastName2',
                'iban': ''}
        form = BankUserUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_clean_methods(self):
        data = {'first_name': '   FirstName123   ',
                'last_name': '   123LastName   ',
                'iban': '  IQ98nbiq850123456789012 '}
        form = BankUserUpdateForm(data=data)
        form.is_valid()
        self.assertEquals('FIRSTNAME123', form.clean_first_name())
        self.assertEquals('123LASTNAME', form.clean_last_name())
        self.assertEquals('IQ98NBIQ850123456789012', form.clean_iban())

