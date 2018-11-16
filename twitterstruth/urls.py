from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('success', views.success, name='success'),
]