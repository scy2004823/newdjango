from django.shortcuts import render
from django.http import HttpResponse
from .models import DailyActivity
from rest_framework import viewsets
from .serializers import DailyActivitySerializers
from rest_framework import permissions


class DailyActivityModelViewSet(viewsets.ModelViewSet):
    queryset = DailyActivity.objects.all()
    serializer_class = DailyActivitySerializers

    permission_classes = [permissions.AllowAny]
