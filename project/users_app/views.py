from re import L
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from users_app.forms import UserRegisterForm, UserEditForm, LoginForm


def registration_view(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponse('Пользователь успешно создан')
    else:
        register_form = UserRegisterForm()
        return render(request, 'users_app/registration.html', {'register_form': register_form})


class UserEditView(View):
    def get(self, request):
        user = request.user
        user_form = UserEditForm(instance=user)
        return render(request, 'users_app/user_edit.html', context={'user_form': user_form})

    def post(self, request):
        user_form = UserEditForm(request.POST)
        if user_form.is_valid():
            user_form.save()
        return render(request, 'users_form/user_edit.html', context={'user_form': user_form})


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'users_app/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Вы успешно вошли в систему')
                else:
                    login_form.add_error('__all__', 'Ошибка! Проверьте правильность написания логина и пароля')
            else:
                login_form.add_error('__all__', 'Ошибка! Проверьте правильность написания логина и пароля')
        else:
            login_form = LoginForm()
            return HttpResponse('Данные формы не валидны')
        return HttpResponse('Вы не смогли войти в систему')
        # return render(request, 'users_app/login.html', {'login_form': login_form})


def logout_user(request):
    logout(request)
    return HttpResponse('Вы успешно вышли из под своей учетной записи')
