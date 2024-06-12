from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FriendRequest
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        

    def validate_email(self, value):
        # Define your email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Check if the email matches the regex pattern
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Invalid email format")
        
        # Check if the email is already taken
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already in use")
        
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
  
  
    
class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    # to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('id','from_user', 'to_user', 'status')
