import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import JoinQuizForm
from .models import Quiz
#from .utils import connect_to_mongodb
from .quiz_sessions import current_sessions, all_answers


def validate_activation(request):
    return HttpResponse("Django app is activated!")

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
def display_quiz(request):
    quizzes = Quiz.objects.all()
    return render(request, 'display_quiz.html', {'quizzes': quizzes, 'user': request.user})

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
            messages.error(request, 'Cannot join a room that already has a teacher!')
            return redirect('home')

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
    #db = connect_to_mongodb()

    students_scores = {}
    answers = all_answers
    #answers = db['answer'].find({'session_id': session_id})
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