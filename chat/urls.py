from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, ChatUserViewSet, MessageViewSet, send_message, chat_messages

router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'chatusers', ChatUserViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-message/', send_message, name='send_message'),
    path('chat-messages/<int:id>', chat_messages, name='chat-messages')

]
