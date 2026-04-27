from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('r/<slug:code>', views.tracked_redirect, name='tracked_redirect')
]