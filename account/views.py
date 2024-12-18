from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, UserRegistrationForm

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Успішний вхід на сайт')
                else:
                    return HttpResponse('Заборонений акаунт')
            else:
                return HttpResponse('Неправильний логін чи пароль')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Створити новий об'єкт користувача
            # але поки не зберігати його
            new_user = user_form.save(commit=False)
            # Встановити обраний пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Зберегти об'єкт User
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
 