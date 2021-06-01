import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = 'users_online'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'connect_message',
                'message': json.dumps(
                    {'username': self.user.username, 'is_logged_in': True}
                ),
            },
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'connect_message',
                'message': json.dumps(
                    {'username': self.user.username, 'is_logged_in': False}
                ),
            },
        )
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.close()

    # Receive message from room group
    def connect_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'chat_message', 'message': message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))


class CeleryConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'celery_events'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.close()

    # Receive message from room group
    def task_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))
