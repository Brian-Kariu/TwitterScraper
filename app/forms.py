from django import forms

from .models import TweetData


class TweetForm(forms.ModelForm):

    class Meta:
        model = TweetData
        fields = ['username']


class LikeForm(forms.ModelForm):

    class Meta:
        model = TweetData
        fields = ['id']
