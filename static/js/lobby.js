socket = io();

socket.on('refresh', function() {
    location.reload();
});

$("#create_lobby").click(function() {
    socket.emit("create_lobby");
});

$("#leave_lobby").click(function() {
    socket.emit("leave_lobby");
});

$("#join_lobby").click(function() {
    socket.emit("join_lobby", {code: $("#code").val()});
});

