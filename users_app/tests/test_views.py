from django.test import TestCase
from django.contrib.auth.models import User


class RegistrationUserTest(TestCase):
    """Test User registarion page"""

    def setUp(self):
        """Setup for doing tests
        creates dictionary with test user's data
        creates variable for page url

        self.test_user -- dictionary
        self.url -- string"""
        self.test_user = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'test',
            'last_name': 'user'
            }

        self.url = '/register/'

    def test_registration_page_exists(self):
        """Test registration view GET function
        attributes:
        self.url -- string"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/registration.html')

    def test_user_is_created(self):
        """Test registration view POST function
        attributes:
        self.url -- string
        self.test_user -- dictionary"""
        response = self.client.post(self.url, self.test_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sucsessfully')

class EditUserTest(TestCase):
    """Test User edit page"""
    def setUp(self):
        """Setup for doing tests
        creates dictionary with test user's data
        creates variable for page url
        creates test user in database. Sets password for the test user

        self.test_user -- dictionary
        self.url -- string
        self.user -- User database instance"""
        self.test_user = {
                'username': 'testuser',
                'password1': 'testpassword',
                'password2': 'testpassword',
                'first_name': 'test',
                'last_name': 'user'
                }

        self.url = '/edit/'
        self.user = User.objects.create(username=self.test_user['username'])
        self.user.set_password(self.test_user['password1'])
        self.user.save()


    def test_edit_page_exists(self):
        """Test user edit view GET function
        attributes:
        self.url -- string
        self.user -- User object

        Logs user then tests page's response"""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/user_edit.html')

    def test_edit_page_post_method(self):
        """Test user edit view POST function
        attributes:
        self.url -- string
        self.user -- User object

        Logs user then tests page's response"""
        self.client.force_login(self.user)
        response = self.client.post(self.url,
                                    {'first_name': self.test_user['first_name'],
                                     'last_name': self.test_user['last_name']})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/user_edit.html')


class LoginUserTest(TestCase):
    """Test Login page View"""

    def setUp(self):
        """Setup for doing tests
        creates dictionary with test user's data
        creates variable for page url
        creates test user in database. Sets password for the test user

        self.test_user -- dictionary
        self.url -- string
        self.user -- User database instance"""
        self.test_user = {
                'username': 'testuser',
                'password1': 'testpassword',
                'password2': 'testpassword',
                'first_name': 'test',
                'last_name': 'user'
                }

        self.url = '/login/'
        self.user = User.objects.create(username=self.test_user['username'])
        self.user.set_password(self.test_user['password1'])
        self.user.save()

    def test_login_page_get_method(self):
        """Test user login view GET function
        attributes:
        self.url -- string
        self.user -- User object

        Tests page's response"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/login.html')

    def test_login_page_post_method(self):
        """Test user login view POST function
        attributes:
        self.url -- string
        self.user -- User object

        Tests page's POST request response"""
        response = self.client.post(self.url,
                                    {'username': self.test_user['username'],
                                     'password': self.test_user['password1']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sucsessfully')


class LogoutUserTest(TestCase):
    """Test Logout page View"""

    def setUp(self):
        """Setup for doing tests
        creates dictionary with test user's data
        creates variable for page url
        creates test user in database. Sets password for the test user

        self.test_user -- dictionary
        self.url -- string
        self.user -- User database instance"""
        self.test_user = {
                'username': 'testuser',
                'password1': 'testpassword',
                'password2': 'testpassword',
                'first_name': 'test',
                'last_name': 'user'
                }

        self.url = '/logout/'
        self.user = User.objects.create(username=self.test_user['username'])
        self.user.set_password(self.test_user['password1'])
        self.user.save()

    def test_logout_page(self):
        """Test user logout view GET function
        attributes:
        self.url -- string
        self.user -- User object

        Tests page's response"""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sucsessfully')
