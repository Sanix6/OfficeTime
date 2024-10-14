from rest_framework import serializers
from .models import Visit, Salary
from user.models import User

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['lat_a', 'lon_a']


class ActivityListSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField(read_only=True)  
    user_status = serializers.CharField(source='user.user', read_only=True) 
    user_logo = serializers.ImageField(source='user.logo', read_only=True) 
    visit_is_active = serializers.BooleanField(source='is_active', read_only=True)

    class Meta:
        model = Visit
        fields = [
            'user_full_name', 
            'user_status',
            'user_logo',
            'visit_is_active',
            'time',
        ]

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.time:
            representation['time'] = instance.time.strftime('%H:%M')
        return representation
    


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['data', 'time', 'is_active']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.time:
            representation['time'] = instance.time.strftime('%H:%M')
        return representation
    


class HistorySalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Salary
        fields = ['type', 'salary', 'date']


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    def get_full_name(self, obj):
        if isinstance(obj, User):
            return f"{obj.first_name} {obj.last_name}"
        return None

    class Meta:
        model = User 
        fields = ['full_name', 'logo', 'summ'] 