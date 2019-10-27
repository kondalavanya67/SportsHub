from django.urls import path
from sports import views

app_name = 'sports'

urlpatterns = [
    path('choose_favorites/', views.choose_favorite_sports, name='choose_favorites'),
    path('tournament_list/', views.tournament_list, name='tournament_list'),
    path('create_tournament/', views.create_tournament, name='create_tournament'),
    path('my_tournament/', views.user_tournament, name='my_tournament'),
    path('delete_tournament/<int:t_id>', views.delete_tournament, name='delete_tournament'),
]
