socket = io.connect('http://' + document.domain + ':' + location.port + '/');

socket.on('refresh', () => {
    location.reload();
});

socket.on('no_player', () => {
    $('#chat').val($('#chat').val() + '< ' + 'Недостаточно игроков для начала игры' + ' >' + '\n');
    $('#chat').scrollTop($('#chat')[0].scrollHeight);
});

socket.on('put_msg', (data) => {
    $('#chat').val($('#chat').val() + data.name + ": " + data.msg + '\n');
    $('#chat').scrollTop($('#chat')[0].scrollHeight);
});

socket.on('put_lobby_msg', (data) => {
    console.log('sssssss')
    $('#chat').val($('#chat').val() + '< ' + data.name + ' ' +  data.msg + ' >' +'\n');
});

socket.on('game_redirect', (data) => {
    location.href = "/game/" + data.id
});

socket.on('lobby_redirect', () => {
    location.href = "/"
});

$("#create_lobby").click(() => {
    socket.emit("create_lobby");
});

$("#leave_lobby").click(() => {
    socket.emit("leave_lobby");
});

$("#join_lobby").click(() => {
    socket.emit("join_lobby", {code: $("#code").val()});
});

$("#send_msg").click(() => {
    socket.emit("chat_msg", {msg: $("#msg_text").val()});
    $('#msg_text').val("")
});;

$("#start_game").click(() => {
    socket.emit("start_game");
});
