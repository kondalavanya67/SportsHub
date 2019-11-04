from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from sports.models import Sport, Tournaments, CoachingCenters
from sports.forms import FavoriteSports, TournamentRegistration, CoachingCenterRegistration
from django.urls import reverse


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


def tournament_list(request):
    tournaments = Tournaments.objects.all()
    tournamentForm = TournamentRegistration()
    if request.method == 'POST':
        form = TournamentRegistration(data=request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            name = form.cleaned_data['name']
            des = form.cleaned_data['description']
            s_date = form.cleaned_data['start_date']
            e_date = form.cleaned_data['end_date']
            location = form.cleaned_data['location']
            Tournaments.objects.create(name=name, description=des, start_date=s_date, end_date=e_date,
                                       location=location, user=user)
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        user_tournaments = Tournaments.objects.filter(user=user)
        return render(request, 'sports/tournament_list.html',
                      {'Tournaments': tournaments, 'tornamentFourm': tournamentForm,
                       'User_Tournaments': user_tournaments})
    return render(request, 'sports/tournament_list.html',
                  {'Tournaments': tournaments, 'tornamentFourm': tournamentForm})


@login_required
def delete_tournament(request, t_id):
    if t_id:
        user = User.objects.get(pk=request.user.pk)
        try:
            t = Tournaments.objects.get(pk=t_id, user=user)
            t.delete()
        except:
            pass
    return HttpResponseRedirect(reverse('sports:tournament_list'))


def coaching_centers_list(request):
    coaching_centers = CoachingCenters.objects.all()
    coaching_centersForm = CoachingCenterRegistration()
    if request.method == 'POST':
        form = CoachingCenterRegistration(data=request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            name = form.cleaned_data['name']
            des = form.cleaned_data['description']
            add = form.cleaned_data['address']
            CoachingCenters.objects.create(name=name, description=des,
                                           address=add, user=user)
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        user_coaching_centers = CoachingCenters.objects.filter(user=user)
        return render(request, 'sports/user_coaching_centers.html',
                      {'user_coaching_centers': user_coaching_centers, 'coaching_centers': coaching_centers, 'coaching_centersForm': coaching_centersForm})
    return render(request, 'sports/coaching_centers_list.html',
                  {'coaching_centers': coaching_centers, 'coaching_centersForm': coaching_centersForm})


@login_required
def delete_coaching_centers(request, c_id):
    if c_id:
        user = User.objects.get(pk=request.user.pk)
        try:
            t = CoachingCenters.objects.get(pk=c_id, user=user)
            t.delete()
        except:
            pass
    return HttpResponseRedirect(reverse('sports:coaching_centers_list'))
