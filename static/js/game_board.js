var prev_color = "black";

socket = io.connect('http://' + document.domain + ':' + location.port + '/');

socket.on('moved', (data) => {
    prev_color = data.color;
    if (data.color == "white"){
        $("#td_" + data.row + "_" + data.col).text("o");
    } else {
        $("#td_" + data.row + "_" + data.col).text("x");
    }

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