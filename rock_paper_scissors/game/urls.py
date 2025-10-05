from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play_game, name='play_game'),
    path('autoplay/', views.autoplay_game, name='autoplay_game'),
    path('reset/', views.reset_stats, name='reset_stats'),
]