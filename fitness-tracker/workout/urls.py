from django.urls import path
from . import views

urlpatterns = [
    path("workout/", views.WorkoutViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name="workout"),
    path("workout/<int:pk>/", views.WorkoutViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name="workout")
]
