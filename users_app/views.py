from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from users_app.forms import UserRegisterForm, UserEditForm, LoginForm
from django.utils.translation import gettext_lazy as _


def registration_view(request):
    """View for registration page

    POST method:
    takes username and password from UserRegisterForm
    authenticates the user with them
    sets permission's group 'Common_users'
    logins the user
    """
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # user.groups.set(['Common_users'])
            login(request, user)
            return HttpResponse(_('The user created sucsessfully'))
        else:
            return HttpResponse(_('Please check if login and password is correct'))
    else:
        register_form = UserRegisterForm()
        return render(request, 'users_app/registration.html', {'register_form': register_form})


class UserEditView(View):
    """View for user edit page"""

    def get(self, request):
        """GET method for user edit page
        Uses instance athribute for the user form for pre filling the form"""
        user = request.user
        user_form = UserEditForm(instance=user)
        return render(request, 'users_app/user_edit.html', context={'user_form': user_form})

    def post(self, request):
        """POST method for user edit page
        Saves form's data"""
        user_form = UserEditForm(request.POST)
        if user_form.is_valid():
            user_form.save()
        return render(request, 'users_app/user_edit.html', context={'user_form': user_form})


class LoginView(View):
    """View for the user login page"""

    def get(self, request):
        """GET method for the user login page"""
        login_form = LoginForm()
        return render(request, 'users_app/login.html', {'login_form': login_form})

    def post(self, request):
        """POST method for the user login page

        Takes username and password from LoginForm
        Performs validation
        Logins user"""
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse(_('You sucsessfully entered the system'))
                else:
                    login_form.add_error('__all__', _('Error! Please check if login and password is correct'))
            else:
                login_form.add_error(_('__all__', 'Error! Please check if login and password is correct'))
        else:
            login_form = LoginForm()
            return HttpResponse(_('Form data is not valid'))
        return HttpResponse(_('You did not enter the system'))
        # return render(request, 'users_app/login.html', {'login_form': login_form})


def logout_user(request):
    """View for the logout page
    Performs user logout"""
    logout(request)
    return HttpResponse(_('You sucsessfully exited the system'))
