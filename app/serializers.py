import base64

import requests
from django.conf import Settings, settings
from django.core.mail import EmailMessage
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from app.models import TweetData


def send_email():
    subject = "New Tweets"
    msg = "There are new tweets"
    from_email = settings.EMAIL_HOST_USER
    to = settings.RECIPIENT_ADDRESS
    res = EmailMessage(subject, msg, from_email, [to])
    if(res == 1):
        msg = "Mail Sent Successfully."
    else:  
        msg = "Mail Sending Failed."
    return print(msg)


def twitter_authentication():
    # Reformat the keys and encode them
    key_secret = '{}:{}'.format(
        settings.CONSUMER_KEY, Settings.CONSUMER_KEY_SECRET).encode('ascii')
    # Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)
    # Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()['access_token']
    stream_headers = {
        'Authorization': 'Bearer {}'.format(access_token)   
    }
    return stream_headers


def get_username(username):
    name = username
    stream_headers = twitter_authentication()
    stream_url = "https://api.twitter.com/2/users/by/username/" + name 
    stream_resp = requests.get(stream_url, headers=stream_headers)
    stream_data = stream_resp.json()
    data = stream_data.get('data')
    user_id = data.get('id')
    return user_id


def fetch_tweet(username):
    user_id = get_username(username)
    stream_headers = twitter_authentication()
    stream_url = "https://api.twitter.com/2/users/" 
    + user_id + "/tweets?tweet.fields=public_metrics,created_at" 
    stream_resp = requests.get(stream_url, headers=stream_headers)
    stream_data = stream_resp.json()
    data = stream_data.get('data')
    return data


def like_tweet(tweet):
    # TODO This should be the logged in user's account
    user_id = "1463574475543396363"
    stream_headers = twitter_authentication()
    body={
        "tweet_id": tweet
    }
    stream_url="https://api.twitter.com/2/users/" + user_id + "/likes" 
    stream_resp=requests.post(stream_url, headers=stream_headers, body=body)
    stream_data=stream_resp.json()
    data=stream_data.get('data')
    print(data)
    return data

def trending_tweets():
    stream_headers = twitter_authentication()
    stream_url = "https://api.twitter.com/2/tweets/search/recent?max_results=10&query=chelsea&tweet.fields=public_metrics,created_at&expansions=author_id" 
    stream_resp = requests.get(stream_url, headers=stream_headers)
    stream_data = stream_resp.json()
    data = stream_data.get('data')
    if data is None:
        raise Response("This user has no Tweets")
    else:
        for i in data:
            username_url="https://api.twitter.com/2/users?ids=" 
            + i.get('author_id')
            username_resp=requests.get(username_url, headers=stream_headers)
            username_data=username_resp.json()
            user_data=username_data.get('data')
            for j in user_data:
                name = j.get('name')
            public_metrics = i.get('public_metrics')
            likes = public_metrics.get("like_count")
            TweetData.objects.create(
                id=i.get('id'), text=i.get('text'), username=name, 
                likes=likes, created_at=i.get('created_at'))
            send_email()
    return data


class TweetSerializer(ModelSerializer):
    
    class Meta:
        model = TweetData
        fields="__all__"
        read_only_fields=('id', 'text', 'public_metrics', 'likes', 'created_at')

    def create(self, validated_data):
        name_data=validated_data.get('username')
        data=fetch_tweet(name_data)
        if data is None:
            raise serializers.ValidationError("This user has no Tweets")
        else:
            for i in data:
                if TweetData.objects.filter(id=i.get('id')).exists():
                    serializer=TweetData.objects.last()
                
                else:
                    public_metrics = i.get('public_metrics')
                    likes = public_metrics.get("like_count")
                    serializer = TweetData.objects.create(
                        id=i.get('id'), text=i.get('text'), username=name_data,
                        likes=likes, created_at=i.get('created_at'))
                    # send_mail(data)
        return serializer

