from PIL import Image, ImageDraw

STONES = {'black': 'X', 'white': 'O'}
SIZES = {19: 1000 / 20, 13: 1000 / 14, 9: 1000 / 10}


def init_game(size):
    # Инициализирует начало игры, возвращая словарь информацией о текущей игре
    board = []
    for row in range(size):
        for col in range(size):
            board.append({'row': row, 'col': col, 'value': ' '})
    return board


def get_updated_board(board, move, color):
    r, c = move
    old_board = board.copy()
    board = reformat_board_to_matrix(board)
    board[r][c] = color
    for row in range(len(board)):
        for col in range(len(board)):
            kill_surrounded_stones(row, col, board)
    board = reformat_board_to_lst(board)

    updated = []
    for o, n in zip(old_board, board):
        if o["value"] != n["value"]:
            updated.append(n)

    return board, updated


def get_updated_game(game, move):
    board = game['board']
    color = game['color']
    if move != 'pass':
        x, y = move
        board = reformat_board_to_matrix(board)
        board[y][x] = color
        for row in range(len(board)):
            for col in range(len(board)):
                kill_surrounded_stones(row, col, board)
        render_board(board)
        board = reformat_board_to_lst(board)
    return {'board': board, 'color': change_color(color), 'counter': game['counter'] + 1}


def kill_surrounded_stones(row, col, board):
    # Уничтожает камни, окруженные камнями противника
    checked = set()
    if is_surrounded(row, col, checked, board):
        for i, j in checked:
            if board[i][j] == ' ':
                checked.remove((i, j))

            board[i][j] = ' '

    return checked


def is_surrounded(row, col, checked, board):
    # Рекурсивная функция, проверяющая, окружен ли камень
    checked.add((row, col))
    if board[row][col] == ' ':
        return False

    res = []
    for i, j in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        i, j = row + i, col + j
        if not (outside_the_field(i, j, len(board))):
            if board[i][j] == ' ':
                return False
            elif board[i][j] == board[row][col] and (i, j) not in checked:
                res.append(is_surrounded(i, j, checked, board))

    if all(node for node in res):
        return True
    return False


def outside_the_field(row, col, size):
    return not (0 <= row < size and 0 <= col < size)


def reformat_board_to_matrix(board):
    # Преобразует список словарей поля в матрицу
    size = board[-1]['row'] + 1
    res_board = [[' ' for j in range(size)] for i in range(size)]
    for elem in board:
        res_board[int(elem['row'])][int(elem['col'])] = elem['value']
    return res_board


def reformat_board_to_lst(board):
    # Преобразует матрицу поля в список словарей
    size = len(board)
    res_board = []
    for row in range(size):
        for col in range(size):
            res_board.append({'row': row, 'col': col, 'value': board[row][col]})
    return res_board