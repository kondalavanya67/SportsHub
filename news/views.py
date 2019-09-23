from django.shortcuts import render
import requests

requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from .models import HeadLine


def scrape(request):
    session = requests.session()
    url = "https://news.google.com/search?q=sports&hl=en-IN&gl=IN&ceid=IN%3Aen"
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    posts = soup.find_all('div', {'class': 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'})

    HeadLine.objects.all().delete()
    for i in posts:
        link = i.find_all('a', {'class': 'DY5T1d'})[0]['href']
        link = "https://news.google.com" + link
        title = i.find_all('a', {'class': 'DY5T1d'})[0].text
        img = i.find('img', {'class': 'tvs3Id QwxBBf'})['src']
        new_healine = HeadLine()
        new_healine.title = title
        new_healine.image_url = img
        new_healine.url = link
        new_healine.save()
    news = HeadLine.objects.all()
    return render(request, 'news/news_list.html', {'news_list': news})
