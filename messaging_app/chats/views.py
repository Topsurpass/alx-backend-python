from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsConversationParticipant, IsMessageSender
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied



class UserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and managing conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]

    def create(self, request):
        """
        Custom endpoint to create a new conversation.
        Accepts a list of participant IDs in the request body.
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "At least two participants are required to create a conversation."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response(
                {"error": "Some participants could not be found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and managing messages.
    """
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticated, IsMessageSender]

    filterset_fields = ['conversation', 'sender']
    search_fields = ['message_body']
    ordering_fields = ['created_at', 'sender']

    def get_queryset(self):
        """
        Filter messages by conversation ID from the nested URL.
        """
        conversation_id = self.kwargs.get('conversation_pk')  # NestedDefaultRouter provides 'conversation_pk'
        if conversation_id:
            return Message.objects.filter(conversation__conversation_id=conversation_id)
        return Message.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Custom endpoint to send a message to an existing conversation.
        """
        conversation_id = kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        if not (sender_id and message_body):
            return Response(
                {"error": "Sender and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sender = get_object_or_404(User, user_id=sender_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='messages-by-user')
    def messages_by_user(self, request, *args, **kwargs):
        """
        Custom endpoint to fetch all messages sent by a specific user within a specific conversation.
        Accepts `user_id` in the query parameters.
        """
        conversation_pk = kwargs.get('conversation_pk')  # Get conversation ID from nested URL
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {"error": "user_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate conversation existence
        conversation = get_object_or_404(Conversation, conversation_id=conversation_pk)
        user = get_object_or_404(User, user_id=user_id)

        # Filter messages by both conversation and sender
        messages = Message.objects.filter(conversation=conversation, sender=user)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

