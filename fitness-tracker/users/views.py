from .models import User
from rest_framework import viewsets
from .serializers import UserSerializers
from rest_framework import permissions

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny]

