import json
from channels.generic.websocket import AsyncWebsocketConsumer


class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

    async def disconnect(self, close_code):
        # Perform any necessary cleanup
        await self.send(text_data='Goodbye! You are now disconnected.')

    async def receive(self, text_data):
        # Handle received messages
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        data = text_data_json['data']

        if action == 'begin quiz':
            await self.begin_quiz(data)
        elif action == 'next quiz':
            await self.next_quiz(data)
        elif action == 'join hall':
            await self.join_hall(data)
        elif action == 'my_event':
            await self.my_event(data)
        elif action == 'my_broadcast_event':
            await self.my_broadcast_event(data)

    async def begin_quiz(self, event):
        # Handle 'begin quiz' event
        pass

    async def next_quiz(self, event):
        # Handle 'next quiz' event
        pass

    async def join_hall(self, event):
        # Handle 'join hall' event
        pass

    async def my_event(self, event):
        # Handle 'my_event' event
        pass

    async def my_broadcast_event(self, event):
        # Handle 'my broadcast event' event
        pass


