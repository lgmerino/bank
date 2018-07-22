from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from users.models import BankUser
from users.forms import BankUserUpdateForm, BankUserCreateForm


class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='adm1', email='adm1@gmail.com', password='adm1')

    def login(self):
        self.client.login(username='adm1', password='adm1')

        session = self.client.session
        session.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('HomeView'))
        self.assertEqual(resp.status_code, 302)

    def test_anonymous_user(self):
        # redirect to login
        response = self.client.get(reverse('HomeView'))
        self.assertEqual(response.status_code, 302)

    def test_logged_user(self):
        # redirect to BankUserListView
        self.login()
        response = self.client.get(reverse('HomeView'))
        self.assertEqual(response.status_code, 302)


class BankUserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        list_iban_account = ['AD1200012030200359100100',
                             'AE070331234567890123456',
                             'AL47212110090000000235698741',
                             'AT611904300234573201',
                             'AZ21NABZ00000000137010001944',
                             'BA391290079401028494',
                             'BE68539007547034',
                             'BG80BNBG96611020345678',
                             'BH67BMAG00001299123456',
                             'BR1800360305000010009795493C1',
                             'BY13NBRB3600900000002Z00AB00',
                             'CH9300762011623852957',
                             'CR05015202001026284066',
                             'CY17002001280000001200527600',
                             'CZ6508000000192000145399',
                             'DE89370400440532013000',
                             'DK5000400440116243',
                             'DO28BAGR00000001212453611324',
                             'EE382200221020145685',
                             'ES9121000418450200051332',
                             'FI2112345600000785',
                             'FO6264600001631634',
                             'FR1420041010050500013M02606',
                             'GB29NWBK60161331926819',
                             'GE29NB0000000101904917',
                             'GI75NWBK000000007099453']

        administrator1 = User.objects\
            .create_user(username='adm1', email='adm1@gmail.com', password='adm1')
        administrator2 = User.objects\
            .create_user(username='adm2', email='adm2@gmail.com', password='adm2')
        for bank_user_num in range(15):
            BankUser.objects.create(
                first_name='FirstName{0}'.format(bank_user_num),
                last_name='LastName{0}'.format(bank_user_num),
                iban=list_iban_account[bank_user_num],
                administrator=administrator1)
        for bank_user_num in range(15, 25):
            BankUser.objects.create(
                first_name='FirstName{0}'.format(bank_user_num),
                last_name='LastName{0}'.format(bank_user_num),
                iban=list_iban_account[bank_user_num],
                administrator=administrator2)

    def login(self):
        self.client.login(username='adm1', password='adm1')

        session = self.client.session
        session.save()

    def test_anonymous_user(self):
        # redirect to login
        response = self.client.get(reverse('BankUserListView'))
        self.assertEqual(response.status_code, 302)

    def test_logged_user(self):
        self.login()
        response = self.client.get(reverse('BankUserListView'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        self.login()
        response = self.client.get('/bank_user/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.login()
        response = self.client.get(reverse('BankUserListView'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login()
        response = self.client.get(reverse('BankUserListView'))
        self.assertTemplateUsed(response, 'bank_user/list.html')

    def test_pagination(self):
        self.login()
        response = self.client.get(reverse('BankUserListView'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.user1 = BankUser.objects.get(first_name='FirstName1')
        self.assertIn(self.user1.first_name, response.content.decode())

    def test_pagination_second_page(self):
        self.login()
        response = self.client.get("{0}?page=2".format(reverse('BankUserListView')))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.user9 = BankUser.objects.get(first_name='FirstName9')
        self.assertIn(self.user9.first_name, response.content.decode())

    def test_html(self):
        self.login()
        response = self.client.get(reverse('BankUserListView'))
        self.user1 = BankUser.objects.get(first_name='FirstName1')
        self.user10 = BankUser.objects.get(first_name='FirstName10')
        self.assertIn(self.user1.first_name, response.content.decode())
        self.assertIn(self.user10.last_name, response.content.decode())


class BankUserDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        list_iban_account = ['AD1200012030200359100100',
                             'AE070331234567890123456']

        administrator1 = User.objects\
            .create_user(username='adm1', email='adm1@gmail.com', password='adm1')
        User.objects.create_user(username='adm2', email='adm2@gmail.com', password='adm2')
        for bank_user_num in range(2):
            BankUser.objects.create(
                first_name='FirstName{0}'.format(bank_user_num),
                last_name='LastName{0}'.format(bank_user_num),
                iban=list_iban_account[bank_user_num],
                administrator=administrator1)

    def setUp(self):
        self.user0 = BankUser.objects.get(first_name='FirstName0')

    def login(self):
        self.client.login(username='adm1', password='adm1')

        session = self.client.session
        session.save()

    def test_404(self):
        self.login()

        response = self.client.get('/bank_user/555555555/')
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user(self):
        # redirect to login
        response = self.client.get(reverse('BankUserDetailView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 302)

    def test_logged_user(self):
        self.login()
        response = self.client.get(reverse('BankUserDetailView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        self.login()
        response = self.client.get("/bank_user/{0}/".format(self.user0.id))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.login()
        response = self.client.get(reverse('BankUserDetailView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login()
        response = self.client.get(reverse('BankUserDetailView', args=[self.user0.id]))
        self.assertTemplateUsed(response, 'bank_user/detail.html')

    def test_html(self):
        self.login()
        response = self.client.get(reverse('BankUserDetailView', args=[self.user0.id]))
        self.assertContains(response, self.user0.first_name)
        self.assertContains(response, self.user0.last_name)
        self.assertContains(response, self.user0.iban)


class BankUserDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        list_iban_account = ['AD1200012030200359100100',
                             'AE070331234567890123456']

        administrator1 = User.objects\
            .create_user(username='adm1', email='adm1@gmail.com', password='adm1')
        User.objects.create_user(username='adm2', email='adm2@gmail.com', password='adm2')
        for bank_user_num in range(2):
            BankUser.objects.create(
                first_name='FirstName{0}'.format(bank_user_num),
                last_name='LastName{0}'.format(bank_user_num),
                iban=list_iban_account[bank_user_num],
                administrator=administrator1)

    def setUp(self):
        self.user0 = BankUser.objects.get(first_name='FirstName0')

    def login(self):
        self.client.login(username='adm1', password='adm1')

        session = self.client.session
        session.save()

    def login_no_valid_user(self):
        self.client.login(username='adm2', password='adm2')

        session = self.client.session
        session.save()

    def test_404(self):
        self.login()

        response = self.client.get('/bank_user/delete/555555555/')
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user(self):
        response = self.client.get(reverse('BankUserDeleteView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 302)

    def test_logged_user(self):
        self.login()
        response = self.client.get(reverse('BankUserDeleteView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 200)

    def test_logged_no_valid_user(self):
        # only the BankUser.administrator can delete it
        self.login_no_valid_user()
        response = self.client.get(reverse('BankUserDeleteView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.login()
        response = self.client.get("/bank_user/delete/{0}/".format(self.user0.id))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.login()
        response = self.client.get(reverse('BankUserDeleteView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login()
        response = self.client.get(reverse('BankUserDeleteView', args=[self.user0.id]))
        self.assertTemplateUsed(response, 'bank_user/delete.html')

    def test_csrf(self):
        self.login()
        response = self.client.get(reverse('BankUserDeleteView', args=[self.user0.id]))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_html(self):
        self.login()
        response = self.client.get(reverse('BankUserDeleteView', args=[self.user0.id]))
        self.assertContains(response, '<form')
        self.assertContains(response, self.user0.first_name)
        self.assertContains(response, self.user0.last_name)
        self.assertContains(response, self.user0.iban)

    def test_post(self):
        administrator1 = User.objects.get(username='adm1')
        new_bank_user = BankUser.objects.create(
            first_name='FirstNameX',
            last_name='LastNameX',
            iban='GT82TRAJ01020000001210029690',
            administrator=administrator1)
        new_bank_user_id = new_bank_user.id

        self.login()
        response = self.client.post(reverse('BankUserDeleteView', args=[new_bank_user_id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(BankUser.DoesNotExist):
            BankUser.objects.get(pk=new_bank_user_id)


class BankUserUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        list_iban_account = ['AD1200012030200359100100',
                             'AE070331234567890123456']

        administrator1 = User.objects\
            .create_user(username='adm1', email='adm1@gmail.com', password='adm1')
        User.objects.create_user(username='adm2', email='adm2@gmail.com', password='adm2')
        for bank_user_num in range(2):
            BankUser.objects.create(
                first_name='FirstName{0}'.format(bank_user_num),
                last_name='LastName{0}'.format(bank_user_num),
                iban=list_iban_account[bank_user_num],
                administrator=administrator1)

    def setUp(self):
        self.user0 = BankUser.objects.get(first_name='FirstName0')

    def login(self):
        self.client.login(username='adm1', password='adm1')

        session = self.client.session
        session.save()

    def login_no_valid_user(self):
        self.client.login(username='adm2', password='adm2')

        session = self.client.session
        session.save()

    def test_404(self):
        self.login()

        response = self.client.get('/bank_user/update/555555555/')
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user(self):
        # redirect to login
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 302)

    def test_logged_user(self):
        self.login()
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 200)

    def test_logged_no_valid_user(self):
        # only the BankUser.administrator can update it
        self.login_no_valid_user()
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.login()
        response = self.client.get("/bank_user/update/{0}/".format(self.user0.id))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.login()
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login()
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        self.assertTemplateUsed(response, 'bank_user/update.html')

    def test_form(self):
        self.login()
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        form = response.context['form']
        self.assertIsInstance(form, BankUserUpdateForm)

    def test_csrf(self):
        self.login()
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_html(self):
        self.login()
        response = self.client.get(reverse('BankUserUpdateView', args=[self.user0.id]))
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="text"', 3)
        self.assertContains(response, self.user0.first_name)
        self.assertContains(response, self.user0.last_name)

    def test_post(self):
        self.login()

        response = self.client.post(reverse('BankUserUpdateView', args=[self.user0.id]),
                                    {'first_name': '  FirstNameX  ',
                                     'last_name': ' LastNameX ',
                                     'iban': '  gl8964710001000206 '})
        self.assertEqual(response.status_code, 302)
        bank_user = BankUser.objects.get(pk=self.user0.id)
        self.assertEqual(bank_user.first_name, 'FIRSTNAMEX')
        self.assertEqual(bank_user.last_name, 'LASTNAMEX')
        self.assertEqual(bank_user.iban, 'GL8964710001000206')
        self.assertEqual(bank_user.administrator.id,
                         int(self.client.session['_auth_user_id']))


class BankUserCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='adm1', email='adm1@gmail.com', password='adm1')

    def login(self):
        self.client.login(username='adm1', password='adm1')

        session = self.client.session
        session.save()

    def test_404(self):
        self.login()

        response = self.client.get('/bank_user/create/555555555/')
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user(self):
        # redirect to login
        response = self.client.get(reverse('BankUserCreateView'))
        self.assertEqual(response.status_code, 302)

    def test_logged_user(self):
        self.login()
        response = self.client.get(reverse('BankUserCreateView'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        self.login()
        response = self.client.get('/bank_user/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.login()
        response = self.client.get(reverse('BankUserCreateView'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login()
        response = self.client.get(reverse('BankUserCreateView'))
        self.assertTemplateUsed(response, 'bank_user/create.html')

    def test_form(self):
        self.login()
        response = self.client.get(reverse('BankUserCreateView'))
        form = response.context['form']
        self.assertIsInstance(form, BankUserCreateForm)

    def test_csrf(self):
        self.login()
        response = self.client.get(reverse('BankUserCreateView'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_html(self):
        self.login()
        response = self.client.get(reverse('BankUserCreateView'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="text"', 3)

    def test_post(self):
        self.login()

        response = self.client.post('/bank_user/create/',
                                    {'first_name': '  FirstNameX  ',
                                     'last_name': ' LastNameX ',
                                     'iban': '  gl8964710001000206 '})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BankUser.objects.latest('id').first_name, 'FIRSTNAMEX')
        self.assertEqual(BankUser.objects.latest('id').last_name, 'LASTNAMEX')
        self.assertEqual(BankUser.objects.latest('id').iban, 'GL8964710001000206')
        self.assertEqual(BankUser.objects.latest('id').administrator.id,
                         int(self.client.session['_auth_user_id']))
