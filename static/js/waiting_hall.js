let role = ""
let nickname = ""
let lobbySocket = undefined

/**
 * The function loads settings based on the user's identity and joins a hall using socket.io if the
 * user is a student.
 */
function loadSetting() {
    const identity = document.querySelector('#identity');
    role = identity.dataset.role;
    nickname = identity.dataset.nickname;

    console.log("You are ", role, " - ", nickname);

    let url = `ws://${window.location.host}/ws/socket-server/`

    lobbySocket = new WebSocket(url)

    lobbySocket.onopen = function () {
        if (identity === 'student') {
            document.getElementById('TeacherBlock').style.display = 'none';
            lobbySocket.send(JSON.stringify({action: 'new_student_join', data: nickname}));
        } else if (identity === 'teacher') {
            lobbySocket.send(JSON.stringify({action: 'new_teacher_join', data: nickname}));
        }
    };

    lobbySocket.onmessage = function (e) {
        let message = JSON.parse(e.data)
        console.log('Message: ', message)
        if (message.action === 'redirect') {
            lobbySocket.send(JSON.stringify({action: 'my_event', data: 'Q1'}));
            window.location.href = "/run_test/0";
        } else if (message.action === 'new_student_join') {
            $('#log').append('<div class="col">' + $('<div/>').text(message.data).html() + '</div>');
        }

    };

    lobbySocket.onclose = function () {
        if (identity === 'student') {
            lobbySocket.send(JSON.stringify({action: 'student_exit', data: nickname}));
        } else if (identity === 'teacher') {
            lobbySocket.send(JSON.stringify({action: 'teacher_exit', data: nickname}));
        }
    };

}

/**
 * The function starts a quiz and emits a signal to begin the quiz if the user is a teacher.
 * @returns nothing (undefined) if the identity is not "teacher". If the identity is "teacher", the
 * function will emit a 'begin quiz' event with the data object {data: "begin quiz now"} and then
 * return.
 */
function startQuiz() {

    if (identity === 'student') {
        lobbySocket.send(JSON.stringify({action: 'quiz_begin', data: nickname}));
        return;
    }
    return;
}
