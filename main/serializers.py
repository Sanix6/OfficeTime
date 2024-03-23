from rest_framework import serializers
from models import *


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['data', 'time', 'status']
