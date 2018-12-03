from django.db import models


# Create your models here.

# Account table
class Account(models.Model):
    id = models.BigIntegerField(primary_key=True)
    real_account = models.BooleanField()
    account_type = models.IntegerField()
    default_profile_pic = models.IntegerField()
    no_name = models.IntegerField()
    no_desc = models.IntegerField()
    lt_30_friends = models.IntegerField()
    gt_1000_friends = models.IntegerField()
    not_geo_located = models.IntegerField()
    three_friends_one_followers = models.IntegerField()
    never_tweeted = models.IntegerField()


# Tweet table
class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=200)
