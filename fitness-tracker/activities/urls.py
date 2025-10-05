
from django.urls import path
from .views import DailyActivityModelViewSet

urlpatterns = [
    path("activity/", DailyActivityModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name="user"),
    path("activity/<int:pk>/", DailyActivityModelViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name="user")
]
