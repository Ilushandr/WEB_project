var sc_width = document.documentElement.clientWidth
var sc_height = document.documentElement.clientHeight
var path = document.location.pathname

var size = '19'
var board_size = Math.min(sc_width, sc_height) - 100
var node_size = board_size / (String(+size + +'1'))

socket = io.connect('http://' + document.domain + ':' + location.port + '/');

var prev_color = 'black'

socket.on('moved', function(data) {
    // Обновляем картинку игровой доски
    prev_color = data.color
    d = new Date()
    $("#board-pic").attr("src", "/static/img/board.png?"+d.getTime())
    var picture = document.getElementById('board-pic')
    var padding = node_size / 2
    picture.style.paddingRight = padding
    picture.style.width = String(board_size) + 'px'
    picture.style.height = String(board_size) + 'px'

    document.getElementById('black-score').innerHTML = 'black: ' + data.score.black
    document.getElementById('white-score').innerHTML = 'white: ' + data.score.white
});

function make_move(move) {
            socket.emit('make_move', {'move': move, 'prev_color': prev_color});
        }

function pass() {
            socket.emit('make_move', {'move': '', 'prev_color': prev_color});
        }

window.onload = window.onresize = function set_size() {
    console.log('resize')
    // После загрузки страницы подстраиваем размеры
    sc_width = document.documentElement.clientWidth
    sc_height = document.documentElement.clientHeight
    board_size = Math.min(sc_width, sc_height) - 100
    node_size = board_size / (String(+size + +'1'))

    var board_container = document.getElementById('board-container')
    var chat_container = document.getElementById('board-container')
    var chat = document.getElementById('chat')
    var picture = document.getElementById('board-pic')
    var table = document.getElementById('table')

    // Задаем размеры игровой доски
    board_container.style.width = String(board_size) + 'px'
    board_container.style.height = String(board_size) + 'px'

    // Задаем отступ для игровой доски
    var padding = (sc_width - board_size) / 2
    board_container.style.marginLeft = padding + 'px'

    // Задаем размеры для чата
    chat.cols = sc_width / 50
    chat.rows = sc_height / 50


    // Задаем размеры и отступ картинки доски
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