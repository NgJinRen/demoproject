from django.db import models


# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=255)

class SearchTitle(models.Model):
    title = models.CharField(max_length=255)

class Tweet(models.Model):
    tweet_id = models. BigIntegerField()
    title = models.CharField(max_length=500)
    created_on = models.DateTimeField()
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()
    search_title_status = models.CharField(max_length=255)
    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)
    search_title = models.ForeignKey(SearchTitle, null=True, on_delete=models.CASCADE)




    