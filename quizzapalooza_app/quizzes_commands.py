import json
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import QuizForm
from .models import Quiz
from .quiz_sessions import current_sessions


@login_required(login_url='/login')
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            # Process the form data
            user = request.user
            form.save(user)  # Customized save()
            messages.success(request, 'Quiz created!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = QuizForm()

    return render(request, 'create_quiz.html', {'user': request.user, 'form': form})

@csrf_exempt
@login_required(login_url='/login')
def delete_quiz(request):
    """
        This function deletes a quiz from the database if the quiz exists and is owned by the current user.
        :return: An empty JSON object.
        """
    if request.method == 'POST':
        quiz_id = json.loads(request.body.decode('utf-8'))['quizId']
        print(request.body.decode('utf-8'))
        print(f"quizID: {quiz_id}")
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            quiz.delete()
            redirect_url = '/display_quiz/'
            messages.success(request, 'Quiz deleted successfully')
            return JsonResponse({'status': 'success', 'redirectUrl': redirect_url})
        except Quiz.DoesNotExist:
            messages.error(request, 'Quiz not found')
            return JsonResponse({'status': 'error', 'message': 'Quiz not found'})
    else:
        messages.error(request, 'Invalid request method')
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required(login_url='/login')
def run_quiz(request):
    session_id = random.randint(20001, 40000)
    while session_id in current_sessions:
        session_id = random.randint(20001, 40000)
    return redirect('start_session', session_id=session_id)

def start_session(request, session_id, nickname=''):
    session_id = int(session_id)

    if request.user.is_authenticated:
        role = 'teacher'
        current_sessions[session_id] = {"teacher": request.user, "students": [], 'answers': []}
        print(current_sessions)
    else:
        role = 'student'
        current_sessions[session_id]["students"].append(nickname)

    identity = {
        'nickname': str(request.user).split("@")[0] if request.user.is_authenticated else nickname,
        'role': role
    }
    students = current_sessions[session_id]["students"]
    teacher_id = str(request.user)
    return render(request, 'waiting_hall.html',
                  {'identity': identity, 'students': students, 'session_id': session_id, 'teacher_id': teacher_id})