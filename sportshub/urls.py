from django.contrib import admin
from django.urls import path, include, re_path
from user_auth import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_page),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
            name='activate'),
    path('user_auth/', include('user_auth.urls')),
    path('admin/', admin.site.urls),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_password.html'),
         name='forgot_pass'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_password_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/(<uidb64>[0-9A-Za-z]+)-(<token>.+)/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html'),
         name='password_reset_complete'),

]
