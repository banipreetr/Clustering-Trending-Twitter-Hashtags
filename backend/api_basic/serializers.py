from rest_framework import serializers
from .models import TrendingTweets

class TrendingTweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingTweets
        fields = ['region']
        
