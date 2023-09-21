import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class DisplayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('display', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('display', self.channel_name)

    async def send_to_display(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'send_to_display',
            'data': data,
        }))

    
    async def receive(self, text_data):
        message_data = json.loads(text_data)
        message = message_data['message']

        await self.send(text_data=json.dumps({'message': message}))
