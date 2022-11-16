from django.http import response
from blogs_app.views import *
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user, get_user_model
from django.contrib.auth.models import User
from django.test import Client
from blogs_app.models import BlogpostModel
from django.contrib.auth.models import Permission

class BlogCreationViewTest(TestCase):
    """Test Blog creation test view

    Required setting permission -- can_post_blogpost"""

    def setUp(self):
        """Sets test data:
        creates:
        self.user -- User object
        self.blog_data -- dictionary, contains data for creating new blogpost
        self.img_data -- string, contains image address for image file"""
        self.url = '/create_blog/'
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        user = get_user_model().objects.get(username="testuser")
        permission = Permission.objects.get(codename='can_post_blogpost')
        user.user_permissions.add(permission)
        user.save()
        self.blog_data = {'title': 'testtitle', 'contents': 'testcontents'}
        self.img_data = 'blogs_app/tests/test_img.png'

    def test_user_created_correctly(self):
        """Test if self.user set correctly"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.has_perm("blogs_app.can_post_blogpost"), True)
        logged_user = self.client.login(username="testuser", password="testpassword")
        self.assertTrue(logged_user)

    def test_page_return_403_if_not_logged(self):
        """Test if PermissionDenied rises if user is not logged"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_page_return_200_if_logged(self):
        """Test if Blog creation view render correctly

        self.user -- User object
        self.url -- string, contains page's URL"""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_app/create_blog.html')

    def test_post_new_blog(self):
        """Test blog creation POST method

        self.user -- User object
        self.url -- string, contains page's URL
        self.blog_data -- dictionary, contains data for blog creation
        self.img_data -- string, contains test_img file path

        Do user login
        Make post with self.blog_data and image img_data
        Check responses
        Check redirection responses"""
        self.client.force_login(self.user)
        with open(self.img_data, 'rb') as img:
            response = self.client.post(self.url,
                                   {'title': self.blog_data['title'],
                                    'contents': self.blog_data['contents'],
                                    'image': img})
        self.assertEqual(response.status_code, 302)
        with open(self.img_data, 'rb') as img:
            redirect_response = self.client.post(self.url,
                                            {'title': self.blog_data['title'],
                                             'contents': self.blog_data['contents'],
                                             'image': img},
                                             follow=True)
        self.assertEqual(redirect_response.status_code, 200)
        self.assertTemplateUsed(redirect_response, 'blogs_app/blog_list.html')
        self.assertContains(redirect_response, 'testtitle')


class BlogListViewTest(TestCase):
    """Test Blogs list page"""

    def test_list_view_get_method(self):
        """Test blog list view get method"""
        url = '/blog/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_app/blog_list.html')


class BlogDetailsViewTest(TestCase):
    """Test Blog detailed view page"""
    def setUp(self):
        """Setting up test data

        self.url -- string
        self.user -- User object, has permission can_post_comment
        self.blog -- BlogpostModel object
        self.comment -- CommentaryModel object

        Create self.user
        Set password for the self.user
        Set permission for the self.user
        Login self.user
        Create self.blog
        Check if self.blog created"""
        self.url = '/blog/1'
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        user = get_user_model().objects.get(username="testuser")
        permission = Permission.objects.get(codename='can_post_comment')
        user.user_permissions.add(permission)
        user.save()
        self.client.force_login(self.user)
        self.blog = BlogpostModel(title='testtitle',
                                  contents='testcontents',
                                  author=self.user)
        self.blog.save()
        self.comment = CommentaryModel.objects.create(author=self.user,
                                                      blogpost=self.blog,
                                                      comment_body="First comment",
                                                      )
        self.comment_data = {'comment_body': 'Second comment'}
        # Test if self.blog is created normaly
        new_blog= BlogpostModel.objects.get(title="testtitle")
        self.assertEqual(new_blog.title, "testtitle")
        self.assertEqual(new_blog.contents, "testcontents")
        self.assertEqual(new_blog.id, 1)

    def test_blog_details_page_response(self):
        """Test blog details page GET response
        self.url -- string, contains page's URL"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_app/blog_details.html')
        self.assertContains(response, 'testtitle')
        self.assertContains(response, 'First comment')

    def test_blog_details_page_post_method(self):
        """Test blog details page POST response
        self.url -- string, contains page's URL
        self.comment_data -- Dictionary, contains data for creating comment"""
        response = self.client.post(self.url, self.comment_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_app/blog_details.html')
        self.assertContains(response, 'testtitle')
        self.assertContains(response, 'First comment')
        self.assertContains(response, 'Second comment')


class UploadCSVFileViewTest(TestCase):
    """Test Uploading CSV file"""
    def setUp(self):
        """Setting up test data

        self.url -- string, contains url address
        self.user -- User object
        self.file_root -- string, contains file address"""
        self.url = '/create_blog/csv'
        self.file_root = 'blogs_app/tests/test_csv.csv'
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        user = get_user_model().objects.get(username="testuser")
        permission = Permission.objects.get(codename='can_post_blogpost')
        user.user_permissions.add(permission)
        user.save()
        self.client.force_login(self.user)

    def test_upload_csv_file_view_get(self):
        """Test Upload csv file GET response"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_app/csv_upload.html')

    def test_upload_csv_file_view_post(self):
        """Test Upload csv file POST response"""
        with open(self.file_root, 'r') as csv:
            response = self.client.post(self.url, {'file': csv})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'blogs_app/csv_upload.html')
        self.assertContains(response, 'Blogs have been created successfully')
