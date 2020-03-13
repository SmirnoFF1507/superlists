from django.urls import reverse
from accounts.models import Token
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from .authentication import PasswordlessAuthenticationBackend
from django.contrib.auth import logout as auth_logout


def send_login_email(request):
    """отправить сообщения для входа в систему"""
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Используйте эту ссылку для входа:\n\n{url}'
    send_mail(
        'Ваша ссылка для Суперблокнота',
        message_body,
        'andreypage@yandex.ru',
        [email]
    )
    messages.success(
        request,
        "Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт."
    )
    return redirect('/')


def login(request):
    """зарегистрировать вход в систему"""
    print(request.GET.get('token'))
    user = PasswordlessAuthenticationBackend.authenticate(request, uid=request.GET.get('token'))
    print(user)
    if user:
        auth.login(request, user)
    return redirect('/')

def logout(request):
 '''выход из системы'''
 auth_logout(request)
 return redirect('/')