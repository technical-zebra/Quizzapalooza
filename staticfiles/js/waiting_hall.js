let role = ""
let nickname = ""


/**
 * The function loads settings based on the user's identity and joins a hall using socket.io if the
 * user is a student.
 */
function loadSetting() {
    role = document.getElementById('identity').dataset.role;
    nickname = document.getElementById('identity').dataset.nickname;
    console.log("You are ",role," - ", nickname);

    let url = `ws://${window.location.host}/ws/socket-server/`

    const lobbySocket = new WebSocket(url)

    lobbySocket.onmessage = function (e){
        let data = JSON.parse(e.data)
        console.log('Data: ', data)
    }

    // if (identity == "student"){
    //     document.getElementById('TeacherBlock').style.display = 'none';
    //
    //     socket.emit('join hall', {data: nickname});
    // }

}

/**
 * The function starts a quiz and emits a signal to begin the quiz if the user is a teacher.
 * @returns nothing (undefined) if the identity is not "teacher". If the identity is "teacher", the
 * function will emit a 'begin quiz' event with the data object {data: "begin quiz now"} and then
 * return.
 */
function startQuiz(){
    var socket = io();
    if (identity == "teacher"){
        socket.emit('begin quiz', {data: "begin quiz now"});
                return;
    }
}

/* This code block is using jQuery to wait for the document to be fully loaded before executing the
code inside the function. It then creates a new socket connection using socket.io and listens for
two events: 'redirect' and 'new student'. */
$(document).ready(function() {
    var socket = io();

    socket.on('redirect', function() {
        socket.emit('my_event', {data: 'Q1'});
        window.location.href = "/run_test/0";
    });

    socket.on('new student', function(msg) {
                $('#log').append('<div  class="col">' + $('<div/>').text(msg.data).html());
    });

});
