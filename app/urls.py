from django.urls import path
# from .views import TweetDataViewSet

from . import views


app_urls = [
    path('tweets/detailed/', views.detailed_tweet, name='detailed_tweet'),
    path('', views.tweet_list, name='home'),
    path('search/form/', views.search_tweet, name='search_tweet'),
]
