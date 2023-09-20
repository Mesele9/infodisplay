import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DisplayConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add('display', self.channel_name))
        
        return self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard('display', self.channel_name))

    def send_to_display(self, event):
        data = event['data']
        async_to_sync(self.send(text_data=json.dumps({
            'type': 'send_to_display',
            'data': data,
        })))