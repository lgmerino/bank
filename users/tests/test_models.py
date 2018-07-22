from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from users.models import BankUser


class BankUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        administrator1 = User.objects.create_user(username='adm1', email='adm1@gmail.com', password='adm1')
        User.objects.create_user(username='adm2', email='adm2@gmail.com', password='adm2')
        BankUser.objects.create(first_name='FirstName1',
                                last_name='LastName1',
                                iban='AD1200012030200359100100',
                                administrator=administrator1)

    def test_bank_user_create(self):
        bank_user1 = BankUser.objects.get(first_name='FirstName1')
        self.assertTrue(isinstance(bank_user1, BankUser))
        bank_user_str = "{0} {1} ({2})".format(bank_user1.first_name,
                                               bank_user1.last_name,
                                               bank_user1.iban)
        self.assertEqual(bank_user1.__str__(), bank_user_str)

    def test_bank_user_update(self):
        administrator1 = User.objects.get(username='adm1')
        administrator2 = User.objects.get(username='adm2')
        bank_user2 = BankUser.objects.create(
                first_name='FirstName4',
                last_name='LastName4',
                iban='HU42117730161111101800000000',
                administrator=administrator1)

        bank_user2.first_name = 'NewFirstName'
        bank_user2.last_name = 'NewLastName'
        bank_user2.iban = 'GR1601101250000000012300695'
        bank_user2.administrator = administrator2
        bank_user2.save()

        bank_user2 = BankUser.objects.get(pk=bank_user2.id)

        self.assertTrue(isinstance(bank_user2, BankUser))
        bank_user_str = "{0} {1} ({2})".format(bank_user2.first_name,
                                               bank_user2.last_name,
                                               bank_user2.iban)
        self.assertEqual(bank_user2.__str__(), bank_user_str)
        self.assertEqual(bank_user2.administrator, administrator2)

    def test_bank_user_delete(self):
        administrator1 = User.objects.get(username='adm1')
        new_bank_user = BankUser.objects.create(
            first_name='FirstNameX',
            last_name='LastNameX',
            iban='HR1210010051863000160',
            administrator=administrator1)
        new_bank_user_id = new_bank_user.id
        new_bank_user.delete()

        with self.assertRaises(BankUser.DoesNotExist):
            BankUser.objects.get(pk=new_bank_user_id)

    def test_bank_user_iban_duplicated(self):
        administrator1 = User.objects.get(username='adm1')
        bank_user1 = BankUser.objects.get(first_name='FirstName1')

        with self.assertRaises(IntegrityError):
            BankUser.objects.create(
                first_name='FirstName3',
                last_name='LastName3',
                iban=bank_user1.iban,
                administrator=administrator1)
