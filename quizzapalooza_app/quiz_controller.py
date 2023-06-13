import json
import random

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import connect_to_mongodb

from .models import Quiz

# - `current_sessions` is an empty list that will be used to store information about currently active
# quiz sessions.
current_sessions = {}


def validate_activation(request):
    return HttpResponse("Django app is activated!")


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import JoinQuizForm, QuizForm


@login_required(login_url='/login')
def home(request):
    return render(request, 'index.html', {'user': request.user})


def join_quiz(request):
    """
    This function allows a student to join a quiz session by providing a session ID and a nickname, and
    performs some validation checks before adding the student to the current session and creating a new
    user in the database.
    """
    if request.method == 'POST':
        form = JoinQuizForm(request.POST)
        if form.is_valid():
            session_id = int(form.cleaned_data['session_id'])
            nickname = form.cleaned_data['nickname']
            print(current_sessions)
            if session_id not in current_sessions.keys():
                messages.error(request, 'Session does not exist!')
            elif nickname in current_sessions[session_id]["students"]:
                messages.error(request, 'Student already exists!')
            else:
                return redirect('start_session_with_nickname', session_id=session_id, nickname=nickname)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = JoinQuizForm()

    return render(request, 'join_quiz.html', {'form': form})


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


@login_required(login_url='/login')
def display_quiz(request):
    quizs = Quiz.objects.all()
    return render(request, 'display_quiz.html', {'quizs': quizs, 'user': request.user})


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


def start_quiz(request, session_id, nickname, qid=0):
    qid = int(qid)
    teacher = current_sessions[session_id]["teacher"]
    teacher_name = str(teacher).split("@")[0]
    quizzes = Quiz.objects.filter(user=teacher)
    quiz_length = len(quizzes)
    quiz = quizzes[0]

    role = "student"
    if request.user.is_authenticated:
        role = "teacher"
        nickname = str(request.user).split("@")[0]
        if nickname != teacher_name:
            messages.error(request, 'Cannot join a room that already have a teacher!')
            redirect('home')

        current_sessions[session_id]["answers"] = [q.answer_id for q in quizzes]

    if len(quizzes) == 0:
        messages.error(request, 'No questions in database')
        return redirect('home')

    quizzes = json.dumps(list(
        Quiz.objects.filter(user=teacher).values("content", "choice_1_content", "choice_2_content", "choice_3_content",
                                                 "choice_4_content")))

    print(f"quizzes: {quizzes}")
    print(f"answers: {current_sessions[session_id]['answers']}")
    return render(request, 'run_quiz.html',
                  {'quizzes': quizzes, 'quiz': quiz, 'quiz_length': quiz_length, 'role': role,
                   'nickname': nickname,
                   'session_id': session_id})


def get_students_scores(session_id):
    db = connect_to_mongodb()

    students_scores = {}
    answers = db['answer'].find({'session_id': session_id})
    for answer in answers:
        student_name = answer['student_name']
        correctness = answer['correctness']
        score = 1 if correctness else 0
        if student_name in students_scores:
            students_scores[student_name] += score
        else:
            students_scores[student_name] = score
    return students_scores


def show_leaderboard(request, session_id):
    students_scores = get_students_scores(session_id)
    ranked_scores = sorted(students_scores.items(), key=lambda x: x[1], reverse=True)
    ranking = []
    for rank, (student_name, score) in enumerate(ranked_scores, start=1):
        print(f"Rank {rank}: {student_name} - Score: {score}")
        ranking.append((rank, student_name, score))

    return render(request, 'leaderboard.html', {'ranking': ranking})


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
