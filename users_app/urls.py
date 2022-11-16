from django.urls import path
from . import views


urlpatterns = [
        path('register/', views.registration_view, name='registration_view'),
        path('edit/', views.UserEditView.as_view()),
        path('login/', views.LoginView.as_view()),
        path('logout/', views.logout_user, name='logout_view'),
        ]
