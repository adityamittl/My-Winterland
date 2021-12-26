from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse
import pandas as pd
import pickle
import os
import json
import bs4 as BeautifulSoup
import requests

path0 = os.getcwd()

path = os.path.abspath(os.path.join(path0, os.pardir))+'\\Netflix Recommendation System\\netflix_titles.csv'
# similarity = pickle.load(open(os.path.abspath(os.path.join(path0, os.pardir))+'\\backend\\similarity.pkl', 'rb'))
# print(similarity)
df = pd.read_csv(path)
index = df['title']
res = index.to_json()
b = json.loads(res)
tags_df = pd.read_csv(os.path.abspath(os.path.join(path0, os.pardir))+'\\Netflix Recommendation System\\tags_df.csv')

def get_poster(name):
    name = name.replace(" ","+")
    base_url = "https://www.imdb.com"
    url = "https://www.imdb.com/find?q="+name
    page = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(page.content, "html.parser")
    res = soup.find_all("table",class_ = 'findList')[0]
    s_url = res.find(class_ = "result_text").find('a')['href']
    page2 = requests.get(base_url+s_url)
    soup2 = BeautifulSoup.BeautifulSoup(page2.content,"html.parser")
    poster_url = BeautifulSoup.BeautifulSoup(requests.get(base_url+soup2.find_all("a",class_="ipc-lockup-overlay ipc-focusable")[0]['href']).content,"html.parser").find_all(class_="MediaViewerImagestyles__PortraitContainer-sc-1qk433p-2 iUyzNI")[0].find("img").attrs["src"]
    return poster_url



# def recommend(title):
#     index = tags_df[tags_df['title'] == title].index[0]
#     print(index)
#     distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

#     recommendations = []

#     for i in distances[1:6]:
#         recommendations.append(tags_df.iloc[i[0]].show_id)

#     return recommendations


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



@api_view(['GET'])
def movie_choose(request):
    if request.method == 'GET':
        return Response(b)




def recommendation(request,slug):
    if request.method == 'GET':
        slug = slug.replace("_"," ")
        # data = {"title": request.data['title']}
        # print(data['title'])
        # resp = recommend(data['title'])
        # resp = recommend(slug)
        # print(resp)
        # res = []
        # for i in resp:
        #     details = df[df['show_id'] == i]
        #     res.append({"title": details['title'].values[0],"description":details['description'].values[0],"rating":details['rating'].values[0],"listed_in":details['listed_in'].values[0],"image":get_poster(details['title'].values[0])})
        # return JsonResponse(json.dumps(res), safe=False)


def homes(request):
    return render(request,"templates/index.html")

def budget(request):
    return render(request,"templates/budget.html")

def donate(request):
    return render(request,"templates/donate.html")

def home(request):
    return render(request,"templates/home.html")

def movie(request):
    return render(request,"templates/movie.html")

def send(request):
    return render(request,"templates/send.html")  

def tracking(request):
    return render(request,"templates/tracking.html")


def trackingDetails(request):
    return render(request,"templates/trackingDetails.html")

def recepie(request):
    return render(request,"templates/recipes.html")