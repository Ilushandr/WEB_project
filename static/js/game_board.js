var prev_color = "black";

socket = io.connect('http://' + document.domain + ':' + location.port + '/');

socket.on('updated', (data) => {
    prev_color = data.color;

    data.events.forEach(function(item, i, arr) {
        if (item.value == "white"){
            $("#td_" + item.row + "_" + item.col).text("o");
        } else if (item.value == "black"){
            $("#td_" + item.row + "_" + item.col).text("x");
        } else {
            $("#td_" + item.row + "_" + item.col).text("");
        }
    });
});

socket.on('other_move', () => {
    console.log("other player move");
});

socket.on('pass_move', (data) => {
    prev_color = data.color;
});

function make_move(row, col) {
    socket.emit('make_move', {row: row, col: col, prev_color: prev_color});
}

function pass() {
    socket.emit('make_move', {row: null, col: null, prev_color: prev_color});
}