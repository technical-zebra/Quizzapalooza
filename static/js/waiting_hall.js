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
    console.log(session_id)
    let url = `ws://${window.location.host}/ws/socket-server/${session_id}/`

    lobbySocket = new WebSocket(url);


    lobbySocket.onmessage = function (e) {
        let message = JSON.parse(e.data);
        console.log('Message: ', message);
        if (message.action === 'begin quiz') {
            window.location.href = startQuizUrl;
        } else if (message.action === 'student join hall') {
            $('#log').append('<div class="col">' + $('<div/>').text(message.data).html() + '</div>');
        } else if (message.action === 'request identity') {
            if (role === 'student') {
                document.getElementById('TeacherBlock').style.display = 'none';
            }
            const action = role === 'teacher' ? 'teacher join hall' : 'student join hall';
            lobbySocket.send(JSON.stringify({action: action, data: { role: role, nickname: nickname, room: session_id.toString()}}));

        }

    };

    lobbySocket.onclose = function () {
        if (role === 'student') {
            lobbySocket.send(JSON.stringify({action: 'student exit', data: nickname}));
        } else if (role === 'teacher') {
            lobbySocket.send(JSON.stringify({action: 'teacher exit', data: nickname}));
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

    if (role === 'teacher') {
        lobbySocket.send(JSON.stringify({action: 'begin quiz', data: {nickname: nickname, session_id: session_id.toString(), teacher_id: teacher_id}}));
        return;
    }
    return "";
}
