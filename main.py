import string
import random
from data import db_session
from data.users import User
from data.users_resource import UsersResource, UsersListResource
from data import db_session
from flask import Flask, render_template, redirect, make_response, jsonify, session, request
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_socketio import SocketIO, emit, join_room
from forms.user import LoginForm, RegisterForm

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
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    if request.method == "POST":
        lobby_id = keygen(16)
    # jobs = db_sess.query(Jobs).all()
    user = {u.id: "".join((u.name)) for u in db_sess.query(User).all()}
    return render_template('index.html', jobs=[], user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            user_manager = login_user(user, remember=form.remember_me.data)
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


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


def main():
    db_session.global_init("db/db.db")

    api.add_resource(UsersListResource, "/api/v2/users")
    api.add_resource(UsersResource, "/api/v2/users/<int:user_id>")

    socketio.run(app, "127.0.0.1", 80)


if __name__ == '__main__':
    main()