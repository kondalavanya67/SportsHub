from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from .forms import  LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db import connection,IntegrityError
import random
from django.contrib.auth.models import User

from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.urls import reverse_lazy

from django import forms

def home_page(request):
    return render(request, "base.html")


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:

            print(user.is_authenticated)
            login(request, user)
            return HttpResponse('login successful')
        else:
            messages.error(request, 'Invalid login credentials')
            print("error")

    return render(request, "login.html", context=context)


def email_verify(form):
    rand_numb = random.randint(10000, 999999)
    global b
    b = str(rand_numb)
    email = [form.data['email']]
    response = send_mail('OTP for email activation', b, 'swathisindhu09@gmail.com', email)
    return b


# User = get_user_model()
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            b = email_verify(form)
            print(b)
            username = form.data['username']
            email = form.data['email']
            password1 = form.data['password']
            context = {
                'username': username,
                'email': email,
                'password': password1,
                'b': b,
            }

            return render(request, 'verify.html', context)
    else:
        form = RegisterForm()
        messages.error(request, 'Invalid login credentials')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


# User = get_user_model()
def new_user_reg(request):
    if b == request.POST['token']:
        if request.method == 'POST':
            username = request.POST.get('username', False)
            email = request.POST.get('email', False)
            password = request.POST.get('password', False)
            new_user = User.objects.create(username=username, email=email)
            new_user.set_password(request.POST['password'])
            new_user.save()
            login(request, new_user)
            print(new_user)
            return HttpResponse('user created')
    else:
        return HttpResponse('Please give correct OTP')

