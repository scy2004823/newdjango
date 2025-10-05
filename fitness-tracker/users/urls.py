from rest_framework import routers
from django.urls import path
from .views import UserModelViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path("user/", UserModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name="user"),
    path("user/<int:pk>/", UserModelViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name="user")
]

urlpatterns += router.urls