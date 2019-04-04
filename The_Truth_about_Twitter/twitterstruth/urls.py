from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

# Source: https://stackoverflow.com/questions/15491727/include-css-and-javascript-in-my-django-template
# Date Accessed: November 2018
urlpatterns = [
    path('', views.home, name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
# End code used
