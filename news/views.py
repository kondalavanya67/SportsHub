import time

from django.shortcuts import render
import requests
from datetime import datetime

requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from .models import HeadLine, LastNewsUpdate


def scrape():
    session = requests.session()
    url = "https://news.google.com/search?q=sports&hl=en-IN&gl=IN&ceid=IN%3Aen"
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    posts = soup.find_all('div', {'class': 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'})
    HeadLine.objects.filter(category="sports").delete()
    for i in posts:
        link = i.find_all('a', {'class': 'DY5T1d'})[0]['href']
        link = "https://news.google.com" + link
        title = i.find_all('a', {'class': 'DY5T1d'})[0].text
        img = i.find('img', {'class': 'tvs3Id QwxBBf'})['src']
        site = i.find('a', {'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).text
        # time = i.find('time', {'class': 'WW6dff uQIVzc Sksgp'}).text
        new_healine = HeadLine()
        new_healine.title = title
        new_healine.image_url = img
        new_healine.url = link
        new_healine.site = site
        # new_healine.time = time
        new_healine.category = "sports"
        new_healine.save()


def scrape_all_sports():
    session = requests.session()
    sports_list = ['cricket', 'football', 'baseball', 'basketball']
    HeadLine.objects.exclude(category="sports").delete()
    for sport in sports_list:
        url = "https://news.google.com/search?q=" + sport + "&hl=en-IN&gl=IN&ceid=IN%3Aen"
        content = session.get(url, verify=False).content

        soup = BeautifulSoup(content, "html.parser")

        posts = soup.find_all('div', {'class': 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'})
        for i in posts:
            link = i.find_all('a', {'class': 'DY5T1d'})[0]['href']
            link = "https://news.google.com" + link
            title = i.find_all('a', {'class': 'DY5T1d'})[0].text
            img = i.find('img', {'class': 'tvs3Id QwxBBf'})['src']
            site = i.find('a', {'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).text
            # time = i.find('time', {'class': 'WW6dff uQIVzc Sksgp'}).text
            new_healine = HeadLine()
            new_healine.title = title
            new_healine.image_url = img
            # new_healine.time = time
            new_healine.category = sport
            new_healine.url = link
            new_healine.site = site
            new_healine.save()


def news_list(request):
    now = datetime.now()
    last_update = LastNewsUpdate.objects.all()
    if len(last_update) == 0:
        print("oops")
        scrape()
        scrape_all_sports()
        LastNewsUpdate.objects.create(last_update=datetime.now())
    else:
        d1_ts = time.mktime(last_update[0].last_update.timetuple())
        d2_ts = time.mktime(now.timetuple())
        if (int(d2_ts - d1_ts) / 60) > 1000:
            scrape()
            scrape_all_sports()
            LastNewsUpdate.objects.all().delete()
            LastNewsUpdate.objects.create(last_update=datetime.now())
    news = HeadLine.objects.filter(category='football')
    slider_1 = news[:4]
    slider_2 = news[4:8]
    blog_1 = news[8:12]
    blog_2 = news[12:16]
    n = 4
    slider_3 = [news[i * n:(i + 1) * n] for i in range((len(news[16:]) + n - 1) // n)]

    return render(request, 'news/news_list.html',
                  {'slider_1': slider_1, 'slider_2': slider_2, 'slider_3': slider_3, 'blog_1': blog_1,
                   'blog_2': blog_2})

