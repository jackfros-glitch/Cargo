from django.contrib.auth.models import User
from rest_framework import serializers

from content.models import Content
from .models import UserActivity

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        

class UserActivitySerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(read_only=True )
    content = serializers.PrimaryKeyRelatedField(queryset= Content.objects.all())
    
    class Meta:
        model = UserActivity
        fields = "__all__"
        read_only_fields = ["timestamp"]
    
