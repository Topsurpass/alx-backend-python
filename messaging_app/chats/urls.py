from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, UserCreateView

# Create a DefaultRouter and register the viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserCreateView, basename='users')

# Include the router URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
