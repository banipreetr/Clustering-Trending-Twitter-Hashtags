from django.db import models

# Create your models here.
class TrendingTweets(models.Model):
    region = models.CharField(max_length=100)
    