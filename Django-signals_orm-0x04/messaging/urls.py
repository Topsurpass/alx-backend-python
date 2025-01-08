from django.urls import path
from .views import delete_user
from .views import conversation_thread

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('thread/<int:message_id>/', conversation_thread, name='conversation_thread'),
    
]
