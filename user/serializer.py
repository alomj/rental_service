from rest_framework import serializers
from .models import Notes, User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        def create(self, validated_data):
            user = User(
                username=validated_data['username'],
                email=validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'description']