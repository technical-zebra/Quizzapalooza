from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import random
import json

from .models import Quiz, Answer
# - `current_students` is an empty dictionary that will be used to store information about currently
# connected students.
current_students = {}

# - `current_sessions` is an empty list that will be used to store information about currently active
# quiz sessions.
current_sessions = []

def validate_activation(request):
    return HttpResponse("Django app is activated!")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import LoginForm, RegistrationForm, JoinQuizForm

def login_view(request):
    """
    This function handles the login process by checking the user's email and password, and if they
    match, logs the user in and redirects them to the home page.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'Incorrect password!')
            else:
                messages.error(request, 'User does not exist!')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    """
    This function logs out the user and redirects them to the login page.
    """
    logout(request)
    return redirect('/login')


def register_view(request):
    """
    This function handles the registration process for a user, checking for valid email and password
    requirements before creating a new user account.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password and confirm_password and password != confirm_password:
                messages.error(request, "Passwords do not match!")

            else:
                user = User.objects.filter(email=email).first()
                if user:
                    messages.error(request, 'Email already exists')
                else:
                    new_user = User.objects.create_user(username=email, email=email, password=password)
                    login(request, new_user)
                    messages.success(request, 'Account created!')
                    return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def join_quiz(request):
    """
    This function allows a student to join a quiz session by providing a session ID and a nickname, and
    performs some validation checks before adding the student to the current session and creating a new
    user in the database.
    """
    if request.method == 'POST':
        form = JoinQuizForm(request.POST)
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            nickname = form.cleaned_data['nickname']

            if session_id not in current_sessions:
                messages.error(request, 'Session does not exist!')
            elif nickname in current_students:
                messages.error(request, 'Student already exists!')
            else:
                current_students[nickname] = 0
                new_student = User(email=f"{nickname}@student", type="student")
                new_student.save()
                login(request, new_student)
                return redirect('views:start_session', session_id=session_id)
    else:
        form = JoinQuizForm()

    return render(request, 'join_quiz.html', {'form': form})



@login_required(login_url='/login')
def home(request):
    return render(request, 'index.html', {'user': request.user})


@login_required(login_url='/login')
def go(request):
    return render(request, 'index.html')


@login_required(login_url='/login')
def create_quiz(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        quiz_mode = request.POST.get('QuizMode')
        if quiz_mode == "MutiChoices":
            choice1 = request.POST.get('choice1')
            choice2 = request.POST.get('choice2')
            choice3 = request.POST.get('choice3')
            choice4 = request.POST.get('choice4')
        else:
            choice1 = request.POST.get('choice1')
            choice2 = request.POST.get('choice2')
            choice3 = ""
            choice4 = ""

        answer = request.POST.get('answer')

        if len(question) < 3:
            messages.error(request, 'Question should be at least 3 characters')
        elif answer not in ["1", "2", "3", "4"]:
            messages.error(request, 'Answer should be "1" or "2" or "3" or "4"')
        elif quiz_mode not in ["MutiChoices", "TrueOrFalse"]:
            messages.error(request, 'Please give a valid quiz mode')
        else:
            new_quiz = Quiz(user_id=request.user.id, content=question, type=quiz_mode, answer_id=answer,
                            choice_1_content=choice1,
                            choice_2_content=choice2, choice_3_content=choice3, choice_4_content=choice4)
            new_quiz.save()
            messages.success(request, 'Quiz created!')

    return render(request, 'create_quiz.html', {'user': request.user})


@login_required(login_url='/quizzapalooza_app/login')
def display_quiz(request):
    quizs = Quiz.objects.all()
    return render(request, 'display_quiz.html', {'quizs': quizs, 'user': request.user})


def run_quiz(request):
    session_id = random.randint(20001, 40000)
    current_sessions.append(session_id)
    current_students = []
    return redirect('start_session', session_id=session_id)


def start_session(request, session_id):
    return render(request, 'waiting_hall.html', {'user': request.user, 'session_id': session_id})


def run_test(request, qid):
    qid = int(qid)
    quizs = Quiz.objects.all()
    if len(quizs) == 0:
        messages.error(request, 'No questions in database')
        return redirect('home')
    return render(request, 'run_quiz.html', {'quiz': quizs[qid], 'length': len(quizs), 'user': request.user})


def get_leaderboard(request):
    sorted_students = dict(sorted(current_students.items(), key=lambda item: item[1], reverse=True))
    print(sorted_students)
    logout(request)
    return render(request, 'leaderboard.html', {'current_students': sorted_students, 'user': request.user})


def send_answer(request):
    """
    This function receives a POST request with answer data, checks if the answer is correct, updates a
    dictionary of current students' scores, and returns an empty JSON response.
    :return: A JSON response with an empty object.
    """
    content = json.loads(request.body)
    ans = content['ans']
    quiz_id = content['quizId']
    nickname = content['nickname']
    quiz = get_object_or_404(Quiz, id=quiz_id)
    print(quiz)
    print(ans)
    if ans == 0:
        correctness = False
        print(f"ans: {ans} correctness: {correctness}")
    else:
        example_ans = quiz.answer_id
        correctness = False
        if ans == example_ans:
            correctness = True
            current_students[nickname] += 1
        print(f"ans: {ans} ex_ans: {example_ans} correctness: {correctness}")

    return JsonResponse({})


def delete_quiz(request):
    """
    This function deletes a quiz from the database if the quiz exists and is owned by the current user.
    :return: An empty JSON object.
    """
    quiz = json.loads(request.body)
    quiz_id = quiz['quizId']
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz:
        if quiz.user_id == request.user.id:
            quiz.delete()

    return JsonResponse({})

