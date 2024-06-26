from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Chat, ChatUser
from .serializers import ChatSerializer, ChatUserSerializer
from rest_framework import permissions


@api_view(['POST'])
def send_message(request):
    chat_id = request.data.get('chatId')
    content = request.data.get('content')
    user = request.user  # Assuming you're using authentication

    # Xabarni saqlash
    message = Message.objects.create(chat_id=chat_id, content=content, user=user)
    serializer = MessageSerializer(message)

    # Xabarni WebSocket guruhiga yuborish
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{chat_id}',
        {
            'type': 'chat_message',
            'message': serializer.data
        }
    )

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatUserViewSet(viewsets.ModelViewSet):
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def chat_messages(request, id):
    messages = Message.objects.filter(chat_id=id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
