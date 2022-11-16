from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from blogs_app.models import BlogpostModel, CommentaryModel, UploadImageModel
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


class TestUserViewSet(APITestCase):
    """Test User view set for API"""

    def setUp(self):
        """Setting up test data and test if it valid
        self.user -- User object
        self.list_url -- string
        self.detail_url -- string"""
        self.list_url = reverse('user-list')
        self.detail_url = '/api/users/1'
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        user = get_user_model().objects.get(username="testuser")
        permission = Permission.objects.get(codename='can_post_blogpost')
        user.user_permissions.add(permission)
        user.save()
        logged_user = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(logged_user)
        self.assertEqual(User.objects.count(), 1)

    def test_user_list_get_method(self):
        """Test if api list view renders correctly"""
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_detail_get_method(self):
        """Test if api list view renders correctly"""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, 200)


class TestBlogpostViewSet(APITestCase):
    """Test Blogpost view set for API"""

    def setUp(self):
        """Setting up test data and check it validity
        self.user -- User object
        self.list_url -- string
        self.detail_url -- string
        self.blogpost -- BlogpostModel object
        self.blogpost_data -- dictonary"""
        self.list_url = reverse('blogpost-list')
        self.detail_url = '/api/blogs/1'
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        user = get_user_model().objects.get(username="testuser")
        permission = Permission.objects.get(codename='can_post_blogpost')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='can_post_comment')
        user.user_permissions.add(permission)
        user.save()
        logged_user = self.client.login(username='testuser',
                                        password='testpassword',
                                        )
        self.assertTrue(logged_user)
        self.assertEqual(User.objects.count(), 1)
        self.blogpost = BlogpostModel.objects.create(title='testblogpost1',
                                                     contents='testcontents1',
                                                     author=self.user)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(BlogpostModel.objects.count(), 1)

        self.blogpost_data = {'title': 'Test post new blogpost',
                              'contents': 'Here we will test if post method is working correctly',
                              }

    def test_blogpost_list_get_method(self):
        """Test if api list view renders correctly"""
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_blogpost_detail_get_method(self):
        """Test if api detail view renders correctly"""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_blogpost_list_post_method(self):
        """Test if api list view posts new blogpost correctly"""
        response = self.client.post(self.list_url,
                                    self.blogpost_data,
                                    format='json',
                                    enforce_csrf_checks=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BlogpostModel.objects.count(), 2)

    def test_blogpost_detail_put_method(self):
        """Test if api list view put blogpost changes correctly"""
        data = {"title": "testblogpost1", "contents": "Changed",}
        response = self.client.put(self.detail_url,
                                   data=data,
                                   format='json',)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BlogpostModel.objects.count(), 1)
        self.assertEqual(BlogpostModel.objects.get(pk=1).contents, 'Changed')

    def test_blogpost_list_delete_method(self):
        """Test if api list view delete blogpost correctly"""
        response = self.client.delete(self.detail_url,
                                    format='json',
                                    enforce_csrf_checks=True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BlogpostModel.objects.count(), 0)


class TestCommentViewSet(APITestCase):
    """Test Comment view set for API"""

    def setUp(self):
        """Setting up test data and check it validity
        self.user -- User object
        self.list_url -- string
        self.detail_url -- string
        self.blogpost -- BlogpostModel object
        self.comment -- CommentaryModel object
        self.comment_data -- dictionary"""
        self.list_url = reverse('comment-list')
        self.detail_url = '/api/comments/1'
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        user = get_user_model().objects.get(username="testuser")
        permission = Permission.objects.get(codename='can_post_blogpost')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='can_post_comment')
        user.user_permissions.add(permission)
        user.save()
        logged_user = self.client.login(username='testuser',
                                        password='testpassword',
                                        )
        self.assertTrue(logged_user)
        self.assertEqual(User.objects.count(), 1)
        self.blogpost = BlogpostModel.objects.create(title='testblogpost1',
                                                     contents='testcontents1',
                                                     author=self.user)
        self.assertEqual(BlogpostModel.objects.count(), 1)
        self.comment = CommentaryModel.objects.create(comment_body='testcomment1',
                                                     blogpost=self.blogpost,
                                                     author=self.user)
        self.assertEqual(CommentaryModel.objects.count(), 1)

        self.comment_data = {'comment_body': 'Test post new comment',
                              'blogpost': '/api/blogs/1',
                              }

    def test_comment_list_get_method(self):
        """Test if api list view renders correctly"""
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_comment_detail_get_method(self):
        """Test if api detail view renders correctly"""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_comment_list_post_method(self):
        """Test if api list view posts new comment correctly"""
        response = self.client.post(self.list_url,
                                    self.comment_data,
                                    format='json',
                                    enforce_csrf_checks=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CommentaryModel.objects.count(), 2)

    def test_comment_detail_put_method(self):
        """Test if api list view put blogpost changes correctly"""
        data = {"comment_body": "Changed comment", "blogpost": "/api/blogs/1",}
        response = self.client.put(self.detail_url,
                                   data=data,
                                   format='json',)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommentaryModel.objects.count(), 1)
        self.assertEqual(CommentaryModel.objects.get(pk=1).comment_body,
                         'Changed comment')

    def test_comment_list_delete_method(self):
        """Test if api list view delete blogpost correctly"""
        response = self.client.delete(self.detail_url,
                                    format='json',
                                    enforce_csrf_checks=True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CommentaryModel.objects.count(), 0)


class TestUploadImageViewSet(APITestCase):
    """Test UploadImage view set for API"""

    def generate_photo_file(self):
        """Generate image file for testing post and put methods"""
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test_img.png'
        file.seek(0)
        return file

    def setUp(self):
        """Setting up test data and check it validity
        self.user -- User object
        self.list_url -- string
        self.detail_url -- string
        self.blogpost -- BlogpostModel object
        self.image -- UploadImageModel object
        self.image_data -- dictionary"""
        self.list_url = reverse('uploadimage-list')
        self.detail_url = '/api/uploadimages/1'
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpassword")
        self.user.save()
        user = get_user_model().objects.get(username="testuser")
        permission = Permission.objects.get(codename='can_post_blogpost')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='can_post_comment')
        user.user_permissions.add(permission)
        user.save()
        logged_user = self.client.login(username='testuser',
                                        password='testpassword',
                                        )
        self.assertTrue(logged_user)
        self.assertEqual(User.objects.count(), 1)
        self.blogpost = BlogpostModel.objects.create(title='testblogpost1',
                                                     contents='testcontents1',
                                                     author=self.user)
        self.assertEqual(BlogpostModel.objects.count(), 1)
        self.image = UploadImageModel.objects.create(blog_post=self.blogpost,
                                                     image='blogs_app/tests/test_img.png')
        self.assertEqual(UploadImageModel.objects.count(), 1)
        # self.content = SimpleUploadedFile("blogs_app/tests/test_img.png", "filecontentstring")
        self.photo_file = self.generate_photo_file()
        self.image_data = {'blog_post':'/api/blogs/1',
                           'image': self.photo_file}

    def test_uploadimage_list_get_method(self):
        """Test if api list view renders correctly"""
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_uploadimage_detail_get_method(self):
        """Test if api detail view renders correctly"""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_uploadimage_list_post_method(self):
        """Test if api list view posts new uploadimage correctly"""
        response = self.client.post(self.list_url,
                                    self.image_data,
                                    format='multipart',
                                    enforce_csrf_checks=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UploadImageModel.objects.count(), 2)

    def test_uploadimage_detail_put_method(self):
        """Test if api list view put uploadimage changes correctly"""
        response = self.client.put(self.detail_url,
                                   data=self.image_data,
                                   format='multipart',)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UploadImageModel.objects.count(), 1)

    def test_uploadimage_list_delete_method(self):
        """Test if api list view delete blogpost correctly"""
        response = self.client.delete(self.detail_url,
                                    format='json',
                                    enforce_csrf_checks=True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(UploadImageModel.objects.count(), 0)
