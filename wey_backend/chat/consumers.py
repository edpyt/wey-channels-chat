import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.http import JsonResponse

from account.models import User
from chat.models import Conversation, ConversationMessage
from chat.serializers import ConversationMessageSerializer


class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    # Receive message from websocket
    async def receive(self, text_data=None, bytes_data=None):
        my_message = json.loads(text_data)
        user_id, pk_conv, message = my_message  # [user, conversation pk, body]

        # Need sync_to_async function for django sync code
        #
        # It's all from the chat/api.py/conversation_send_message
        user = await sync_to_async(User.objects.get)(id=user_id)

        conversation = await sync_to_async(Conversation.objects.filter) \
            (users__in=[user])

        conversation = await sync_to_async(conversation.get)(pk=pk_conv)

        async for us in conversation.users.all():
            if us != user:
                sent_to = us

        conversation_message = await sync_to_async(ConversationMessage.objects.create)(
            conversation=conversation,
            body=message,
            created_by=user,
            sent_to=sent_to
        )

        serializer = ConversationMessageSerializer(conversation_message)

        # Send message to room group
        await self.channel_layer.group_send(self.room_name,
                                            {'type': 'chat_message',
                                             'message': serializer.data})

        # await self.send_json(serializer.data)

    async def disconnect(self, event):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        message = event['message']
        await self.send_json(message)
