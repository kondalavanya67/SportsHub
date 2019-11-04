from django.urls import path
from sports import views

app_name = 'sports'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('choose_favorites/', views.choose_favorite_sports, name='choose_favorites'),
    path('tournament_list/', views.tournament_list, name='tournament_list'),
    path('delete_tournament/<int:t_id>', views.delete_tournament, name='delete_tournament'),
    path('coaching_centers_list/', views.coaching_centers_list, name='coaching_centers_list'),
    path('delete_coaching_centers/<int:c_id>', views.delete_coaching_centers, name='delete_coaching_centers'),
]
