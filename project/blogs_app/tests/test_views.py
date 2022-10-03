from blogs_app.views import *
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.models import User
from django.test import Client


class BlogCreationViewTest(TestCase):

    # def setUp(self):
        # user_data = {
        #         'username': 'testuser',
        #         'password': 'testpassword'
        #         }
        # user = User.objects.create(username='testuser', password='testpassword')

    def test_if_user_is_logged(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        username = 'testuser'
        password = 'testpassword'
        user = authenticate(username=username, password=password)
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(get_user(self.client).is_authenticated)
        # response = self.client.login(username='testuser', password='testpassword')
        # self.assertTrue(response)

    # def test_blogcreationview_exists_at_desired_location(self):
    #     url = reverse('create_blog')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Создание записи блога')
    #     self.assertTemplateUsed(response, 'blogs_app/create_blog.html')
