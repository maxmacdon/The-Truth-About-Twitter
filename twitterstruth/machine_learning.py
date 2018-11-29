import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()


from twitterstruth.models import Account


for acc in Account.objects.all():
    print(acc)
