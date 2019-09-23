from django.http import HttpResponse
from django.shortcuts import render
from sports.models import Sport
from sports.forms import FavoriteSports


def choose_favorite_sports(request):
    favorites = FavoriteSports()
    all_sports = Sport.objects.all()
    if request.method == 'POST':
        favorites = FavoriteSports(request.POST)
        user = request.user
        print(user)
        sport = Sport.objects.create(user=user, name=favorites.cleaned_data['name'])
        sport.save()
        print('Sved')
        return HttpResponse('Form saved')

    print('rendering....')
    return render(request, 'sports/choose_favorites.html', {'sports': all_sports})
