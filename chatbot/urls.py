from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # must url for chatbot( helping in js file /chatbot-response/ )
    path("chatbot-response/", views.chatbot_response, name="chatbot-response"),
]
