from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        # Extract groups and permissions from validated_data if provided
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])

        # Create the user and hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )
        
        return user

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields ='__all__'
        
    def get_fullname(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model."""
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'

