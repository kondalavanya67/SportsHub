from django.urls import path
from user_auth import views

app_name = 'user_auth'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register_user/', views.register_user, name='register_user'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_user, name='logout_user')
]
