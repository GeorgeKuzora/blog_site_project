# from django.test import TestCase
# from django.contrib.auth import login, User
#
#
# class RegistrationUserTest(TestCase):
#
#     TEST_USER = {
#             'username': 'testuser',
#             'password': 'testpassword',
#             'first_name': 'test',
#             'last_name': 'user'
#             }
#
#     URL = '/register/'
#
#     def test_registration_page_exists(self):
#         response = self.client.get(self.URL)
#         # self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users_app/registration.html')
#
#     # def test_user_is_created(self):
#     #     response = self.client.post((self.URL, {'register_form': self.TEST_USER})) #{'username': self.TEST_USER['username'], 'password1': self.TEST_USER['password'], 'password2': self.TEST_USER['password'], 'first_name': self.TEST_USER['first_name'], 'last_name': self.TEST_USER['last_name']}))
#     #     # self.assertEqual(response.status_code, 200)
#     #     current_user = response.context
#     #     print(current_user)
#     #     self.assertContains(current_user, self.TEST_USER['username'])
#
#
# class EditUserTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         TEST_USER = {
#                 'username': 'testuser',
#                 'password1': 'testpassword',
#                 'password2': 'testpassword',
#                 'first_name': 'test',
#                 'last_name': 'user'
#                 }
#
#         URL = '/register/'
#
#         new_user = User.objects.create(TEST_USER)
#         login(request, new_user)
#
#     def test_edit_page_exists(self):
#         response = self.client.get(self.URL)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users_app/user_edit.html')
