from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("index", views.index),
    path("blogs", views.blogs),
    path("blogs/<int:id>", views.blog_details),
]
