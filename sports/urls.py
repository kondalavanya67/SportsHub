from django.urls import path
from sports import views

app_name = 'sports'

urlpatterns = [
    path('choose_favorites/', views.choose_favorite_sports, name='choose_favorites'),
]
