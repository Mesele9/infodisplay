from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .custom_encoder import CustomJSONEncoder

class DisplayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('display', self.channel_name)
        return self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('display', self.channel_name)

    async def send_to_display(self, event):
        data = event['data']
        data_json = json.dumps(data, cls=CustomJSONEncoder)
        await self.send(data_json)

