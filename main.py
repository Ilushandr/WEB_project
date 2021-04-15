import string
import random
from flask import Flask, render_template, redirect, make_response, jsonify, session, request
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from data import db_session
from data.users import User
from data.users_resource import UsersResource, UsersListResource
from data import db_session
from forms.user import LoginForm, RegisterForm
import data.Game as Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
socketio = SocketIO(app)

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


def keygen(l):
    alphabet = string.ascii_letters + string.digits
    rand_string = ''.join([random.choice(alphabet) for _ in range(l)])
    return rand_string


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/')
def index():
    lobby_id = current_user.lobby_id if current_user.is_authenticated else None
    return render_template('index.html', lobby_id=lobby_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@socketio.on('create_lobby')
def create_lobby():
    db = db_session.create_session()

    lobby_id = keygen(16)
    usr = db.query(User).filter(User.id == current_user.id).first()
    usr.lobby_id = lobby_id
    db.commit()
    join_room(lobby_id)

    emit("refresh")


@socketio.on('leave_lobby')
def leave_lobby():
    db = db_session.create_session()

    usr = db.query(User).filter(User.id == current_user.id).first()
    leave_room(usr.lobby_id)
    usr.lobby_id = None
    db.commit()

    emit("refresh")


@socketio.on('join_lobby')
def join_lobby(data):
    db = db_session.create_session()

    lobby_id = data["code"]
    usr = db.query(User).filter(User.id == current_user.id).first()
    usr.lobby_id = lobby_id
    db.commit()
    join_room(lobby_id)

    emit("refresh")


@app.route('/game/<int:size>')
def game(size):
    # Запускаем игру, так сказать
    # В session['game'] пихаем словарь с доской, цветом (который щас ходит) и счетчиком
    session['game'] = Game.init_game(size)
    return render_template('game.html', title='Игра', size=size)


@socketio.on('move')
def move(message):
    move = message['move']
    if move != '':
        # Апдейтим карту, если юзер сходил
        y, x = list(map(int, move.split('-')))
        session['game'] = Game.get_updated_game(session['game'], move=(x, y))
    else:
        # Если юзер пропустил ход, то просто менеям цвет (игрока то бишь)
        session['game'] = Game.get_updated_game(session['game'], move='pass')

    emit('moved', {'success': 'OK'})


def main():
    db_session.global_init("db/db.db")

    api.add_resource(UsersListResource, "/api/v2/users")
    api.add_resource(UsersResource, "/api/v2/users/<int:user_id>")

    socketio.run(app, "127.0.0.1", 80)


if __name__ == '__main__':
    main()
