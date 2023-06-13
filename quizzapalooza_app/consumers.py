import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import connect_to_mongodb
from .quiz_controller import current_sessions


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
            group_name = data['session_id']

            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'broadcast_message',
                    'action': 'begin quiz',
                    'data': data['session_id'],
                }
            )
            print(f'create_record: {data}')
            await self.create_record(data)

        elif message_action == 'next quiz':
            group_name = data['session_id']
            question_num = data['qid']

            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'broadcast_message',
                    'action': 'next quiz',
                    'data': question_num,
                }
            )


        elif message_action == 'student join hall' or message_action == 'teacher join hall':
            print(
                f"role_data: {data}, message_action: {message_action}, {message_action == 'student join hall' or 'teacher join hall'}, {message_action == 'answer quiz'}")
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


        elif message_action == 'answer quiz':
            print(f'create_answer: {data}')
            await self.create_answer(data)

    async def broadcast_message(self, event):
        print(f'broadcast_message: {event}')

        await self.send(text_data=json.dumps({
            "action": event['action'],
            "data": event['data']
        }))

    async def create_record(self, data):
        db = connect_to_mongodb()
        try:
            session_number = int(data.get('session_id'))
            teacher_name = data.get('nickname')
            teacher_id = data.get('teacher_id')

            record = {
                'session_number': session_number,
                'teacher_name': teacher_name,
                'teacher_id': teacher_id
            }
            db['record'].insert_one(record)
        except Exception as e:
            print(f"Unable to save record: {data}, Error: {str(e)}")

    async def create_answer(self, data):
        db = connect_to_mongodb()
        try:
            user_choice = data.get('ans')
            question_id = data.get('quizId')
            nickname = data.get('nickname')
            session_id = data.get('session_id')
            correctness = user_choice == current_sessions[session_id]['answers'][question_id]

            answer = {
                'session_id': session_id,
                'user_choice_id': user_choice,
                'question_id': question_id,
                'correctness': correctness,
                'student_name': nickname
            }
            db['answer'].insert_one(answer)
        except Exception as e:
            print(f"Unable to save answer: {data}, Error: {str(e)}")
