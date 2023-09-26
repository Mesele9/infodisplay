import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DisplayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('display', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('display', self.channel_name)

    async def send_to_display(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def receive(self, text_data):
        pass
