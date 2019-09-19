from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_page
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include


from .views import home_page, login_page,user_register, new_user_reg

from django.contrib.auth import views as auth_views


urlpatterns = [


    url(r'^login/$', login_page, name='login' ),
    url(r'^register/$', user_register, name='user_register'),
    url(r'^new_user_reg/$', new_user_reg, name='new_user_reg'),
 ]