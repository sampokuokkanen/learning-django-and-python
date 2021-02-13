import uuid
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from accounts.models import Token
from django.contrib import messages


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for Harakka',
        f'Use this to log in: {url}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in"
    )
    return render(request, 'login_email_sent.html')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(request, uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
