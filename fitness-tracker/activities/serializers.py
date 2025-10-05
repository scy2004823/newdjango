from rest_framework import serializers
from .models import DailyActivity

class DailyActivitySerializers(serializers.ModelSerializer):
    class Meta:
        model = DailyActivity
        fields = ('__all__')