from django.template.loader import render_to_string
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime


# Create your tests here.
from .models import Dreams, User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
# import selenium

# data for test enviroment
usernames = [ 'alla', 'anna', 'urbunkatun']
# create dreams
dreams = {}
for user in usernames:
    dreams[user] = {}
    dreams[user]['dream_subject'] = 'user-' + user + '_user_dream_id-'
    dreams[user]['dream_text'] = 'user-' + user + '_user_dream_id-'+ 'oooo XXXXX ogooooo'



class DreamsTests(TestCase):
    """Create users"""

    def create_user(self, username='test'):

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = User(username=username)
            user.set_password('password' + username)
            user.save()
            self.assertEquals(
                user,
                User.objects.get(username=username),
            )

    def create_dream(self, user_dream_id=1, username='test'):
        self.create_user(username)     # include previous test
        user = User.objects.get(username=username)
        dream = Dreams(dream_subject='user-' + username + 'user_dream_id-' + str(user_dream_id) + 'test_dream',
                       dream_text ='user-' + username + 'user_dream_id-'+ str(user_dream_id) + 'oooo XXXXX ogooooo',
                       user=user)
        dream.save()

        self.assertEquals(str(user), username,)
        self.assertEquals(str(dream.dream_subject), 'user-' + username + 'user_dream_id-' + str(user_dream_id) +
                          'test_dream')
        self.assertEquals(str(dream.dream_text), 'user-' + username + 'user_dream_id-' + str(user_dream_id) +
                          'oooo XXXXX ogooooo')
        self.assertEquals(str(dream.user), username)
        self.assertLess(dream.dream_date, timezone.now())

    def registration(self, username):
        # GET
        response = self.client.get(reverse('users:register'))
        self.assertEquals(response.status_code, 200)
        with self.assertTemplateUsed('users/registration.html'):
            render_to_string('users/registration.html')
        # POST
        response = self.client.post(reverse('users:register'), {'username' : username,
                                                                'password1' : 'password' + username,
                                                                'password2' : 'password' + username})
        self.assertRedirects(response, reverse('users:login'))

    def create_dreams(self, username, dream_subj):

        user = User.objects.get(username=username)
        dream = Dreams(dream_subject= dreams.get(username).get('dream_subject') + '_subj-' + dream_subj,
                       dream_text = dreams.get(username).get('dream_text') + ' subj-' + dream_subj,
                       user=user)
        dream.save()
        dream_id = dream.id
        dream = Dreams.objects.get(pk=dream_id)
        self.assertEquals(str(dream.dream_subject), dreams.get(username).get('dream_subject') + '_subj-' + dream_subj)
        self.assertEquals(str(dream.dream_text), dreams.get(username).get('dream_text')+ ' subj-' + dream_subj)
        self.assertEquals(str(dream.user), username)
        self.assertLess(dream.dream_date, timezone.now(), msg='dream.dream_date=' + str(timezone.now()) +
                                                                ' timezone.now=' + str(timezone.now()))

    def create_env(self):
        """
        create test environment, using previous tests
        """
        # create users and dreams
        # self.test_create_dream(username='nun', user_dream_id=1)
        # self.test_create_dream(username='nun', user_dream_id=2)
        # self.test_create_dream(username='nan', user_dream_id=2)

        # register user and dreams
        for i in usernames:
            self.registration(i)
            # create dreams for every user
            for add_subj in ['1', '2', '3']:
                self.create_dreams(i, add_subj)

    def dreams_view(self, username):
        #
        response = self.client.post(reverse('users:login'), {'username' : username,
                                                            'password' : 'password' + username})
        response = self.client.get(reverse('users:dreams'))
        # check number of dreams from create_env()
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            # no dreams for frong user
            self.assertEquals(response.context, None,
                              msg='dreams number=' + str(response.context))
        else:
            self.assertEquals(len(response.context['all_dreams']), len(Dreams.objects.filter(user=user)),
                              msg='dreams number=' + str(len(response.context['all_dreams'])))
            for dream in response.context['all_dreams']:
                self.assertEquals(dream.user, user, msg='foreign dream' + str(dream))
        self.client.logout()


class ViewsTests(DreamsTests):

    def test_view_with_no_dreams(self):
        """
        If no  exist, an appropriate message should be displayed.
        """

        response = self.client.get(reverse('users:dreams'))
        # self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('users:login') + '?next=' + reverse('users:dreams'), msg_prefix=str(response))
        # self.assertContains(response, "No dreams")
        self.assertIsNone(response.context)

    def test_view_dream_deatail(self, pk=1):
        """dream id is equal to number in url"""

        self.create_env()
        all_dreams_ids = [ i.id for i in Dreams.objects.all()]
        # non authtoritaid user, acces to dream, should be redirected to login
        for dream_id in all_dreams_ids:
            response = self.client.get(reverse('users:dream_details',  args=(dream_id,)))
            self.assertEquals(response.status_code, 302, msg=str(response.status_code))
            self.assertRedirects(response, reverse('users:login') + '?next=/users/' + str(dream_id) + '/dream')
        for username in usernames:
            user_dreams_ids = [ i.id for i in Dreams.objects.filter(user__username=username)]
            foreign_dreams = list(set(all_dreams_ids) - set(user_dreams_ids))
            response = self.client.post(reverse('users:login'), {'username' : username,
                                                            'password' : 'password' + username})
            # own dreams should be available
            for dream_id in user_dreams_ids:
                response = self.client.get(reverse('users:dream_details',  args=(dream_id,)))
                self.assertEquals(response.status_code, 200, msg=str(response.status_code))
            # foreign dreams 'forbidden'
            for dream_id in foreign_dreams:
                response = self.client.get(reverse('users:dream_details',  args=(dream_id,)))
                self.assertEquals(response.status_code, 403, msg=str(response.status_code))


    def test_login_view(self):
        self.create_env()

        for url in [ 'users:login']:
            response = self.client.get(reverse(url))
            form = AuthenticationForm()
            self.assertEquals(response.status_code, 200)
            with self.assertTemplateUsed('registration/login.html'):
                render_to_string('registration/login.html')

            # check login in db
            for username in usernames:
                login_result = self.client.login(username=username, password='password' + username)
                self.assertTrue(login_result, msg=str(login_result))
                # check redirect on home page
                user_id = User.objects.get(username=username).id
                response = self.client.post(reverse('users:login'), {'username' : username,
                                                                    'password' : 'password' + username})
                self.assertRedirects(response, reverse('users:home'), msg_prefix=str(response))
                # check user home page
                response = self.client.get(response.url)
                self.assertEquals(response.context['user'].username, username, msg=str(response.context['user'].username))
                self.assertEquals(response.context['user'].id, user_id, msg=str(response.context['user'].id))


    def test_dream_authorization(self):
        self.create_env()
        for username in usernames:
            self.dreams_view(username)
        self.dreams_view('wrong_user')


















class MySeleniumTests(LiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_login(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()