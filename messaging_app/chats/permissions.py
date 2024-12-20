from rest_framework.permissions import BasePermission

class IsConversationParticipant(BasePermission):
    """
    Custom permission to ensure users can only access conversations they are a part of.
    """
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(id=request.user.id).exists()

class IsMessageSender(BasePermission):
    """
    Custom permission to ensure users can only access messages they sent.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender
