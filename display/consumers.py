from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DisplayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('display', self.channel_name)
        return self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('display', self.channel_name)

    async def send_to_display(self, event):
        data = event['data']
        self.send(text_data=json.dumps({
            'type': 'send_to_display',
            'data': data,
        }))