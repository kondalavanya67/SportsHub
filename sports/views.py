from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from sports.models import Tournaments, CoachingCenters, TournamentJoin
from news.models import LastNewsUpdate, HeadLine
from sports.forms import FavoriteSports, TournamentRegistration, CoachingCenterRegistration, TournamentJoinForm
from django.urls import reverse
from news.views import scrape, scrape_all_sports
from datetime import datetime
import time

from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from sports.serializers import TournamentSerializer, JoinTournamentSerializer


def homepage(request):
    now = datetime.now()
    last_update = LastNewsUpdate.objects.all()
    if len(last_update) == 0:
        scrape()
        scrape_all_sports()
        LastNewsUpdate.objects.create(last_update=datetime.now())
    else:
        d1_ts = time.mktime(last_update[0].last_update.timetuple())
        d2_ts = time.mktime(now.timetuple())
        if (int(d2_ts - d1_ts) / 60) > 30:
            scrape()
            scrape_all_sports()
            LastNewsUpdate.objects.all().delete()
            LastNewsUpdate.objects.create(last_update=datetime.now())
    news = HeadLine.objects.filter(category="sports")
    slider_1 = news[:4]
    slider_2 = news[4:8]
    blog_1 = news[8:12]
    blog_2 = news[12:16]
    n = 4
    slider_3 = [news[i * n:(i + 1) * n] for i in range((len(news[16:]) + n - 1) // n)]

    return render(request, 'sports/homepage.html',
                  {'slider_1': slider_1, 'slider_2': slider_2, 'slider_3': slider_3, 'blog_1': blog_1,
                   'blog_2': blog_2})


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
        join = TournamentJoin.objects.filter(user=user)
        joined_pk = []
        for i in join:
            joined_pk.append(i.tournament.pk)
        tournaments = Tournaments.objects.exclude(pk__in=joined_pk)
        join_tornamnets = Tournaments.objects.filter(pk__in=joined_pk)
        return render(request, 'sports/tournament_list.html',
                      {'Tournaments': tournaments, 'tornamentFourm': tournamentForm,
                       'User_Tournaments': user_tournaments, 'joined_tournaments': join_tornamnets})
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
    coaching_centersForm = CoachingCenterRegistration()
    if request.method == 'POST':
        form = CoachingCenterRegistration(data=request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            name = form.cleaned_data['name']
            des = form.cleaned_data['description']
            street = form.cleaned_data['street_name']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            contact = form.cleaned_data['phone_num']
            area = form.cleaned_data['area']
            email = form.cleaned_data['mail']
            CoachingCenters.objects.create(name=name, description=des,
                                           user=user, mail=email, phone_num=contact, pincode=pincode, state=state, street_name=street, area=area)
    coaching_centers = CoachingCenters.objects.all()
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        user_coaching_centers = CoachingCenters.objects.filter(user=user)
        return render(request, 'sports/coaching_centers_list.html',
                      {'user_coaching_centers': user_coaching_centers, 'coaching_centers': coaching_centers,
                       'coaching_centersForm': coaching_centersForm})
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


@api_view(['GET'])
def tournamentsList(request):
    if request.method == 'GET':
        snippets = Tournaments.objects.all()
        serializer = TournamentSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def tournamentsJoin(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # t = Tournaments.objects.get(name=data['tournament'])
        # data['tournament'] = t.pk

        # tournament = get_object_or_404(Tournaments, title=request.data.get('tournament'))

        serializer = JoinTournamentSerializer(data=data)
        print(data)
        if serializer.is_valid():
            print('User Joined')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def join_Tournament(request, t_id):
    joinForm = TournamentJoinForm()
    if t_id:
        tourna = Tournaments.objects.get(pk=t_id)
        if request.method == 'POST':
            joinForm = TournamentJoinForm(request.POST)
            if joinForm.is_valid():
                name = joinForm.cleaned_data['name']
                phone_num = joinForm.cleaned_data['phoneNumber']
                mail = joinForm.cleaned_data['mail']

                if request.user.is_authenticated:
                    user = User.objects.get(pk=request.user.pk)
                    TournamentJoin.objects.create(user=user, tournament=tourna, name=name, mail=mail,
                                                  phoneNumber=phone_num)
                    tourna.no_of_joined += 1
                    tourna.save()
                else:
                    TournamentJoin.objects.create(tournament=tourna, name=name, mail=mail, phoneNumber=phone_num)
                    tourna.no_of_joined += 1
                    tourna.save()
                return HttpResponseRedirect(reverse('sports:tournament_list'))
        return render(request, 'sports/join_tournament.html', {'joinform': joinForm, 'tournament': tourna})


def leave_Tournament(request, t_id):
    if t_id:
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            joined_tournament = TournamentJoin.objects.get(user=user, tournament_id=t_id)
            joined_tournament.delete()
            tournament = Tournaments.objects.get(pk=t_id)
            tournament.no_of_joined -= 1
            tournament.save()
    return HttpResponseRedirect(reverse('sports:tournament_list'))
