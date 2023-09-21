import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DisplayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the WebSocket consumer to the 'display' group
        await self.channel_layer.group_add('display', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket consumer from the 'display' group when disconnected
        await self.channel_layer.group_discard('display', self.channel_name)

    async def send_to_display(self, event):
        # Send data received from the channel to the WebSocket client
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def receive(self, text_data):
        # Handle any incoming messages from the WebSocket client (if needed)
        pass
