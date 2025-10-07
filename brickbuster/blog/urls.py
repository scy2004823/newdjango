from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    HomeView,
    PostAddAPI,
)
urlpatterns = [
    # path('', views.home, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('scoreboard', PostListView.as_view(), name='scoreboard'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user/add_score', views.add_score, name='add-score'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('api/add-post', PostAddAPI.as_view(), name='post-api'),
]
