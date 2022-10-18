from django.http import response
from blogs_app.views import *
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.models import User
from django.test import Client
from blogs_app.models import BlogpostModel


class BlogCreationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        self.c = Client()

    def test_user_created_correctly(self):
        new_user = User.objects.get(username="testuser")
        self.assertEqual(new_user.username, "testuser")

    def test_user_login_correctly(self):
        logged_user = self.c.login(username="testuser", password="testpassword")
        self.assertTrue(logged_user)

    def test_page_return_405_if_not_logged(self):
        url = '/create_blog/'
        response = self.c.get(url)
        self.assertEqual(response.status_code, 403)

    def test_page_return_200_if_logged(self):
        self.c.force_login(self.user)
        url = '/create_blog/'
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_app/create_blog.html')

    def test_post_new_blog(self):
        self.c.force_login(self.user)
        url = '/create_blog/'
        with open('blogs_app/tests/test_img.png', 'rb') as img:
            response = self.c.post(url, {'title': "testtitle", 'contents': "testcontents", 'image': img})
        self.assertEqual(response.status_code, 302)
        with open('blogs_app/tests/test_img.png', 'rb') as img:
            redirect_response = self.c.post(url, {'title': "testtitle", 'contents': "testcontents", 'image': img}, follow=True)
        self.assertEqual(redirect_response.status_code, 200)
        self.assertTemplateUsed(redirect_response, 'blogs_app/blog_list.html')
        self.assertContains(redirect_response, 'testtitle')

        # Blogmodel = BlogpostModel.objects.get(title="testtitle")
        # id = Blogmodel.id
        # blog_url = '/blog/' + str(id) + '/'
        # blog_response = self.c.get(blog_url)
        # self.assertEqual(blog_response.status_code, 200)


class BlogDetailsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        self.c = Client()
        self.c.force_login(self.user)
        self.blog = BlogpostModel(title='testtitle', contents='testcontents', author=self.user)
        self.blog.save()


    def test_blog_created_correctly(self):
        new_blog= BlogpostModel.objects.get(title="testtitle")
        self.assertEqual(new_blog.title, "testtitle")
        self.assertEqual(new_blog.contents, "testcontents")
        self.assertEqual(new_blog.id, 1)

    # def test_blog_details_page_response(self):
    #     self.c.force_login(self.user)
    #     url = '/blog/1/'
    #     response = self.c.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertTemplateUsed(response, 'blogs_app/blog_list.html')
    #     self.assertContains(response, 'testtitle')


class UploadCSVFileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        self.c = Client()
        self.c.force_login(self.user)

    def test_upload_csv_file_view_get(self):
        url = '/create_blog/csv'
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_app/csv_upload.html')

    def test_upload_csv_file_view_post(self):
        url = '/create_blog/csv'
        with open('blogs_app/tests/test_csv.csv', 'r') as csv:
            response = self.c.post(url, {'file': csv})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'blogs_app/csv_upload.html')
        self.assertContains(response, 'Блоги были успешно созданы')
