var sc_width = document.documentElement.clientWidth
var sc_height = document.documentElement.clientHeight
var path = document.location.pathname

var size = path.split('/')[2]
var board_size = Math.min(sc_width, sc_height) - 100
var node_size = board_size / (String(+size + +'1'))

socket = io.connect('http://' + document.domain + ':' + location.port + '/');

socket.on('moved', (data) => {
    if (data.color == "white"){
        $("#td_" + data.row + "_" + data.col).text("o")
    } else {
        $("#td_" + data.row + "_" + data.col).text("x")
    }

});

function make_move(row, col) {
    socket.emit('make_move', {row: row, col: col});
}

function pass() {
            socket.emit('move', {row: null, col: null});
        }


window.onload = function set_size() {
    // После загрузки страницы подстраиваем размеры
    var board_container = document.getElementById('board-container')
    var picture = document.getElementById('board-pic')
    var table = document.getElementById('table')

    board_container.style.width = String(board_size) + 'px'
    board_container.style.height = String(board_size) + 'px'

    var padding = (sc_width - board_size) / 2
    board_container.style.marginLeft = padding + 'px'

    var padding = node_size / 2
    picture.style.paddingRight = padding
    picture.style.width = String(board_size) + 'px'
    picture.style.height = String(board_size) + 'px'

    table.style.marginLeft = String(node_size / 2) + 'px'
    table.style.marginTop = String(node_size / 2) + 'px'

    // Устанавливаем размеры для клеток таблицы игровой доски
    for (var row=0; row < size; row++){
        for (var col=0; col < size; col++){
            var id = 'td_{row}_{col}'.replace('{row}', row).replace('{col}', col)
            document.getElementById(id).style.width = String(node_size) + 'px'
            document.getElementById(id).style.height = String(node_size) + 'px'
        }
    }
}