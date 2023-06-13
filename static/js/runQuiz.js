let answer = 0;
let quizSocket = undefined;

let timerId;
let timeoutId;
let sec = 7;


function startCountdown() {
    timerId = setInterval(setTimerText, 1000);
    timeoutId = setTimeout(() => {
        clearInterval(timerId);
        console.log("Countdown finished! And you are " + role + " !");
        hideChoices(true);
    }, sec * 1000);
}

function resetCountdown() {
    clearInterval(timerId);
    clearTimeout(timeoutId);
    sec = 7;
    document.getElementById('js_timer').innerHTML = '00:' + (sec.toString().length > 1 ? sec : ('0' + sec)) + ' s';
}


function setTimerText() {
    sec = sec - 1;
    document.getElementById('js_timer').innerHTML = '00:' + (sec.toString().length > 1 ? sec : ('0' + sec)) + ' s';
}

/**
 * The function loads settings and hides the teacher block if the user is a student.
 */
function loadSetting() {

    startCountdown();

    if (role == "student") {
        document.getElementById('TeacherBlock').style.display = 'none';
    }

    let url = `ws://${window.location.host}/ws/socket-server/${session_id}/`

    quizSocket = new WebSocket(url);

    quizSocket.onmessage = function (e) {
        let message = JSON.parse(e.data);
        console.log('Message: ', message);
        if (message.action === 'next quiz') {
            if (role == "student") {
                quizSocket.send(JSON.stringify({
                    action: 'answer quiz',
                    data: {ans: answer, quizId: qid, nickname: nickname, session_id: session_id}
                }));
            }
            if (qid + 1 >= quiz_length) {
                window.location.href = leaderboardUrl;
            }
            hideChoices(false);
            setAnswer(message.data);
            qid = qid + 1;
            answer = 0;
            resetCountdown();
            startCountdown();
        } else if (message.action === 'request identity') {
            if (role === 'student') {
                document.getElementById('TeacherBlock').style.display = 'none';
            }
            const action = role === 'teacher' ? 'teacher join hall' : 'student join hall';
            quizSocket.send(JSON.stringify({
                action: action,
                data: {role: role, nickname: nickname, room: session_id.toString()}
            }));

        }

    };

    quizSocket.onclose = function () {
        if (role === 'student') {
            quizSocket.send(JSON.stringify({action: 'student exit', data: nickname}));
        } else if (role === 'teacher') {
            quizSocket.send(JSON.stringify({action: 'teacher exit', data: nickname}));
        }
    };

}


/**
 * The function hides certain elements and sets the answer variable if the identity is "student".
 * @param ans - The answer submitted by the student taking the quiz.
 */
function submitAnswer(ans) {

    if (role == "student") {
        hideChoices(true)
        answer = ans
    }

}

function setAnswer(num) {
    let questionContentElements = document.getElementsByClassName('question-content');
    let button1Element = document.getElementsByClassName('button1')[0];
    let button2Element = document.getElementsByClassName('button2')[0];
    let button3Element = document.getElementsByClassName('button3')[0];
    let button4Element = document.getElementsByClassName('button4')[0];

    questionContentElements[0].innerHTML = quizzes[num]['content'];
    button1Element.innerHTML = quizzes[num]['choice_1_content'];
    button2Element.innerHTML = quizzes[num]['choice_2_content'];
    button3Element.innerHTML = quizzes[num]['choice_3_content'];
    button4Element.innerHTML = quizzes[num]['choice_4_content'];
    if (quizzes[num]['choice_3_content'] === '' && quizzes[num]['choice_4_content'] === ''){
        document.getElementsByClassName('button3')[0].style.display = 'none';
        document.getElementsByClassName('button4')[0].style.display = 'none';
    }

}

function hideChoices(state) {
    if (state) {
        document.getElementById('waiting').style.display = 'inline-flex';
        document.getElementsByClassName('button1')[0].style.display = 'none';
        document.getElementsByClassName('button2')[0].style.display = 'none';
        document.getElementsByClassName('button3')[0].style.display = 'none';
        document.getElementsByClassName('button4')[0].style.display = 'none';
    } else {
        document.getElementById('waiting').style.display = 'none';
        document.getElementsByClassName('button1')[0].style.display = 'inline-block';
        document.getElementsByClassName('button2')[0].style.display = 'inline-block';
        document.getElementsByClassName('button3')[0].style.display = 'inline-block';
        document.getElementsByClassName('button4')[0].style.display = 'inline-block';
    }
}


/**
 * The function sends a socket message to begin the next quiz if the user is a teacher.
 * @returns nothing (undefined).
 */
function nextQuiz() {
    if (role == "teacher") {
        quizSocket.send(JSON.stringify({action: 'next quiz', data: {qid: qid + 1, session_id: session_id.toString()}}));
    }
}

