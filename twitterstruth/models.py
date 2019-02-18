from django.db import models


# Create your models here.

# Account table
class Account(models.Model):
    id = models.BigIntegerField(primary_key=True)
    real_account = models.BooleanField()
    account_type = models.IntegerField()
    name = models.CharField(max_length=60)
    screen_name = models.CharField(max_length=16)
    statuses_count = models.IntegerField()
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    favourites_count = models.IntegerField()
    listed_count = models.IntegerField()
    url = models.CharField(max_length=100)
    lang = models.CharField(max_length=25)
    time_zone = models.CharField(max_length=40)
    location = models.CharField(max_length=70)
    default_profile = models.IntegerField()
    default_profile_image = models.IntegerField()
    geo_enabled = models.IntegerField()
    profile_image_url = models.CharField(max_length=240)
    profile_image_url_https = models.CharField(max_length=240)
    profile_banner_url = models.CharField(max_length=100)
    profile_use_background_image = models.IntegerField()
    profile_background_image_url = models.CharField(max_length=240)
    profile_background_image_url_https = models.CharField(max_length=240)
    profile_background_tile = models.IntegerField()
    utc_offset = models.IntegerField()
    protected = models.IntegerField()
    verified = models.IntegerField()
    description = models.CharField(max_length=320)
    lev_distance = models.IntegerField()

