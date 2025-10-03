from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('', views.index, name='index'),
    path('habit/add/', views.create_habit, name='create_habit'),
    path('habit/<int:pk>/', views.habit_detail, name='habit_detail'),
    path('habit/<int:pk>/log/', views.log_habit, name='log_habit'),
    path('habit/<int:pk>/delete/', views.delete_habit, name='delete_habit'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]