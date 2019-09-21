from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from user_auth.forms import UserProfile
from user_auth.models import Profile
from user_auth.tokens import account_activation_token
from user_auth.forms import RegisterForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.mail import EmailMessage
from django.contrib.auth.models import User


def home_page(request):
    return HttpResponse('Temporary Home page')
    # return render(request, "user_auth/base.html")


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponse('login successful')

    return render(request, 'user_auth/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user_auth:login')
    else:
        return HttpResponse('Activation link is invalid!')


def register_user(request):
    form = RegisterForm()
    form_profile = UserProfile()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form_profile = UserProfile(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            # user.is_active = False
            user.save()
            user_profile = Profile.objects.create(user_name=user, location=form_profile.cleaned_data['location'])
            user_profile.save()

            # current_site = get_current_site(request)
            # mail_subject = 'Activate your account.'
            # message = render_to_string('user_auth/activate_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.send()
            # return HttpResponse('Please confirm your email')
            return HttpResponse('Login success')
    return render(request, 'user_auth/register.html', {'form': form, 'form_profile': form_profile})
