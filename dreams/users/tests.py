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

class DreamsTests(TestCase):
    """Create users"""

    def test_create_user(self, username='test'):

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

    def test_create_dream(self, user_dream_id=1, username='test'):
        self.test_create_user(username)     # include previous test
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


class ViewsTests(DreamsTests):

    def test_create_env(self):
        """
        create test environment, using previous tests
        """

        self.test_create_dream(username='nun', user_dream_id=1)
        self.test_create_dream(username='nun', user_dream_id=2)
        self.test_create_dream(username='nan', user_dream_id=2)

    def test_view_with_no_dreams(self):
        """
        If no  exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('users:dreams'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No dreams")
        self.assertQuerysetEqual(response.context['all_dreams'], [])

    def test_view_dream_id(self, pk=1):
        """dream id is equal to number in url"""

        self.test_create_env()
        response = self.client.get('/users/'+ str(Dreams.objects.get(pk=pk).id) +'/dream')

        self.assertEquals(response.status_code, 200, msg='wrog')
        self.assertEquals(response.context['dream_details'],
                          Dreams.objects.get(pk=pk))

    def test_login_view(self):
        self.test_create_env()

        for url in ['users:user', 'users:login']:
            response = self.client.get(reverse(url))
            form = AuthenticationForm()
            self.assertEquals(response.status_code, 200)
            with self.assertTemplateUsed('users/logining.html'):
                render_to_string('users/logining.html')

            # check login in db
            for username in ['nun', 'nan']:
                login_result = self.client.login(username=username, password='password' + username)
                self.assertTrue(login_result, msg=str(login_result))
                # check redirect on home page
                user_id = User.objects.get(username=username).id
                response = self.client.post(reverse('users:user'), {'username' : username,
                                                                    'password' : 'password' + username})
                self.assertRedirects(response, reverse('users:home', args=(user_id,)), msg_prefix=str(response))
                # check user home page
                response = self.client.get(response.url)
                self.assertEquals(response.context['user'].username, username, msg=str(response.context['user'].username))
                self.assertEquals(response.context['user'].id, user_id, msg=str(response.context['user'].id))

    def test_registration(self):
        # GET
        response = self.client.get(reverse('users:register'))
        self.assertEquals(response.status_code, 200)
        with self.assertTemplateUsed('users/registration.html'):
            render_to_string('users/registration.html')
        # POST
        response = self.client.post(reverse('users:register'), {'form.username' : 'ana',
                                                                'form.password1' : 'passwordana',
                                                                'form.password2' : 'passwordana'})
        self.assertRedirects(response, reverse('users:login'))






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