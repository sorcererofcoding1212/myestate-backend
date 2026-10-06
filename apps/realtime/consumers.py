from channels.generic.websocket import AsyncWebsocketConsumer
from json import dumps


class RealtimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def notification(self, event):
        await self.send(text_data=dumps({
            "message": event["message"],
            "type": "INBOX"
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
