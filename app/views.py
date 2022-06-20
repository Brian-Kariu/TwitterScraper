from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from app.models import TweetData
from app.serializers import (fetch_tweet, like_tweet, send_email)

from .forms import LikeForm, TweetForm


def tweet_list(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            like_tweet(id)
    return render(
        request, 'home.html', {'object_list': TweetData.objects.all()})


def detailed_tweet(request):
    return render(
        request, 'detailed_tweet.html', {'object_list': TweetData.objects.all()})


def search_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            data = fetch_tweet(username)
            if data is None:
                return HttpResponseNotFound("Tweet Not Found")
            else:
                for i in data:
                    if TweetData.objects.filter(id=i.get('id')).exists():
                        continue
                    else:
                        public_metrics = i.get('public_metrics')
                        likes = public_metrics.get("like_count")
                        TweetData.objects.create(id = i.get('id'), text = i.get('text'), 
                                                username = username, likes = likes,
                                                created_at = i.get('created_at')) 
            send_email()
            return redirect('home')
    else:
        form = TweetForm
    return render(request, 'search_tweets.html', {'form': form })

def like(request):
    if(request.GET.get('Like')):
        like_tweet( int(request.GET.get('tweet.id')) )
    return render(request,'app/tweets/detailed.html')


