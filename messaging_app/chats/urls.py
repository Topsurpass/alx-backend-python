from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet, UserCreateView

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserCreateView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
