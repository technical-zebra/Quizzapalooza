import json
from channels.generic.websocket import AsyncWebsocketConsumer


class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = str(self.scope["url_route"]["kwargs"]["room_name"])
        print(f'room_name: {self.room_name}')

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'action': 'request identity',
            'message': ''
        }))

    async def disconnect(self, close_code):
        await self.send(text_data='Goodbye! You are now disconnected.')

    async def receive(self, text_data):
        # Handle received messages
        message = json.loads(text_data)
        print(f'test_data: ', text_data)

        message_action = message.get('action')
        data = message.get('data')
        print(f"action: {message_action}, data: {data}")

        if message_action == 'begin quiz':
            group_name = data

            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'broadcast_message',
                    'action': 'begin quiz',
                    'data': data,
                }
            )

        elif message_action == 'next quiz':
            await self.next_quiz(data)

        elif message_action == 'student join hall' or 'teacher join hall':
            role = data['role']
            nickname = data['nickname']
            session_id = data['room']

            await self.send(text_data=json.dumps({
                'action': 'connection established',
                'message': f'Welcome {role} {nickname} join session {session_id}!'
            }))

            if role == 'student':
                await self.channel_layer.group_send(
                    session_id,
                    {
                        'type': 'broadcast_message',
                        'action': 'student join hall',
                        'data': nickname,
                    }
                )

        elif message_action == 'my_event':
            await self.my_event(data)
        elif message_action == 'my_broadcast_event':
            await self.my_broadcast_event(data)

    async def broadcast_message(self, event):
        print(f'broadcast_message: {event}')

        await self.send(text_data=json.dumps({
            "action": event['action'],
            "data": event['data']
        }))

    async def next_quiz(self, event):
        # Handle 'next quiz' event
        pass

    async def my_event(self, event):
        # Handle 'my_event' event
        pass

    async def my_broadcast_event(self, event):
        # Handle 'my broadcast event' event
        pass
