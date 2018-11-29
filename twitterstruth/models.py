from django.db import models


# Create your models here.
class Account(models.Model):
    id = models.IntegerField()
    account_type = models.IntegerField()
    default_profile_pic = models.IntegerField()
    no_name = models.IntegerField()
    no_desc = models.IntegerField()
    lt_30_friends = models.IntegerField()
    gt_1000_friends = models.IntegerField()
    geo_located = models.IntegerField()
    three_friends_one_followers = models.IntegerField()
    never_tweeted = models.IntegerField()