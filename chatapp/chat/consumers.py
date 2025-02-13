import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None  # Initialize room_name to avoid issues in disconnect

        if self.scope["user"].is_authenticated:
            self.sender = self.scope["user"].username
        else:
            await self.close()
            return

        self.receiver = self.scope["url_route"]["kwargs"]["receiver_username"]
        self.room_name = f"chat_{min(self.sender, self.receiver)}_{max(self.sender, self.receiver)}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        if hasattr(self, "room_name"):  # Check if room_name exists before using it
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = self.sender
        receiver = self.receiver
        message = data["message"]

        sender_user = await self.get_user(sender)
        receiver_user = await self.get_user(receiver)

        if sender_user and receiver_user:
            await self.save_message(sender_user, receiver_user, message)

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "receiver": receiver,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "receiver": event["receiver"],
        }))

    @staticmethod
    async def get_user(username):
        try:
            return await User.objects.aget(username=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    async def save_message(sender, receiver, message):
        await Message.objects.acreate(sender=sender, receiver=receiver, message=message)
