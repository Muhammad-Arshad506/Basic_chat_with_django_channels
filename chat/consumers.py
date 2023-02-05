import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# from .models import *
from .serialzer import *


class ChatConsumer(AsyncWebsocketConsumer):
    online_user = []

    async def connect(self):
        try:
            self.user = self.scope["user"].username
            await self.channel_layer.group_add(self.user, self.channel_name)
            await self.accept()
            ChatConsumer.online_user.append(self.user)
            unread_message = await self.get_unread_message(self.user)

            await self.send(json.dumps(unread_message))
        except Exception as e:
            print(e)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user, self.channel_name)
        ChatConsumer.online_user.remove(self.user)
        print(f"user connection is disable {self.user}")
        await self.close(415)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            await self.channel_layer.group_send(data["receiver"],
                                                {
                                                    "type": "chat.message",
                                                    "text": data["text"],
                                                },
                                                )
            await self.message(message=data)
        except Exception as e:
            print(e)

    async def chat_message(self, event):
        await self.send(text_data=event["text"])

    @database_sync_to_async
    def message(self, message):
        message["is_delivered"] = message["receiver"] in ChatConsumer.online_user
        message["sender"] = self.user
        Message.objects.create(**message)

    @database_sync_to_async
    def get_unread_message(self, receiver):
        try:
            messages = Message.objects.filter(receiver=receiver, is_delivered=False)
            serialized_message = MessageSerializer(messages, many=True)
            result = self.get_sender_all_message(serialized_message.data)
            messages.update(is_delivered=True)
            return result
        except Exception as e:
            print(e)
            result = f"failed to get unread message =====> {e}"
            return result

    def get_sender_all_message(self, message):

        required_result = {}
        for i in message:
            if required_result.get(i.get("sender")):
                required_result[i.get("sender")].append(i)
            else:
                required_result[i.get("sender")] = [i]
        return required_result


class GroupConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"].username
        rooms = await self.get_all_group()
        for room in rooms:
            await self.channel_layer.group_add(room,self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.close(code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send(data["receiver"],
                                            {
                                                "type": "chat.message",
                                                "text": data["text"],
                                            },
                                            )
    @database_sync_to_async
    def get_all_group(self):
        room = Group.objects.filter(member=self.scope["id"])
        room_ser = GroupSerializer(room, many=True).data
        return list(room_ser)
    async def chat_message(self, event):
        await self.send(text_data=event["text"])