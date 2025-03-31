from rest_framework import serializers
from .models import Subscription, SubscriptionPlan
from django.utils import timezone
from datetime import timedelta

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all())
    user_id = serializers.IntegerField(source="user.id", read_only=True) 

    class Meta:
        model = Subscription
        fields = ['id', 'user_id', 'plan', 'start_date', 'end_date', 'auto_renew']
        read_only_fields = ['start_date', 'end_date', 'id', 'user_id']
        
    def create(self, validated_data):
        """Ensure start_date is set before saving"""
        validated_data["start_date"] = timezone.now()
        validated_data["end_date"] = validated_data["start_date"] + timedelta(days=validated_data["plan"].duration_days)
        return super().create(validated_data)
