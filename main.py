try:
    import os
    os.mkdir('indexdir')
except BaseException as exc:
    pass

from security.const import *
from forms.forms import *
from data import db_session
from data.users import Users
import films_resource
import users_resource
import comments_resource

import requests
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_recaptcha import ReCaptcha
from flask_restful import Api
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flask import Flask, render_template, redirect, url_for, request
from flask_ngrok import run_with_ngrok
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_SITE_KEY'] = RECAPTCHA_SITE_KEY
app.config['RECAPTCHA_SECRET_KEY'] = RECAPTCHA_SECRET_KEY
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

mail = Mail(app)

recaptcha = ReCaptcha(app=app)

api = Api(app)
api.add_resource(films_resource.FilmsListResource, '/api/films/<token>')
api.add_resource(films_resource.FilmsResource, '/api/films/<token>/<int:films_id>')
api.add_resource(users_resource.UsersListResource, '/api/users/<token>')
api.add_resource(users_resource.UsersResource, '/api/users/<token>/<int:users_id>')
api.add_resource(comments_resource.CommentsListResource, '/api/comments/<token>')
api.add_resource(comments_resource.CommentsResource, '/api/comments/<token>/<int:comment_id>')

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def send_email_to(recipients, text="Test"):
    msg = Message(text, sender=FULL_MAIL_USERNAME, recipients=recipients)
    mail.send(msg)
    return 'success'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(Users).get(user_id)


@app.route("/", methods=['GET', 'POST'])
@app.route("/page/<int:pages>", methods=['GET', 'POST'])
def index(pages=0):
    info = json.loads(requests.get(DOMEN + "/api/films/" + TOKEN).content)['films']
    if pages * 4 > len(info):
        return redirect("/")
    return render_template("index.html", page=pages, info=info)


# Done
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if not recaptcha.verify():
            return render_template("login.html", form=form, message="Подтвердите что вы не робот")
        session = db_session.create_session()
        users = session.query(Users).filter(Users.email == form.email.data).first()
        if users and users.check_password(form.password.data):
            login_user(users, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", form=form)


# Done
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not recaptcha.verify():
            message = "Подтвердите что вы не робот"
            return render_template("register.html", form=form, message=message)
        else:
            not_hash = gen_password()
            password = generate_password_hash(not_hash)
            params = {
                'nickname': form.username.data,
                'email': form.email.data,
                'hashed_password': password,
                'access_level': 1
            }
            info = json.loads(requests.post(DOMEN + "/api/users/" + TOKEN, json=params).content)
            message = ""
            for key in info:
                message += str(info[key]) + "\n"
            if 'success' in info:
                send_email_to([form.email.data], "Ваш пароль от сайта: {}".format(not_hash))
            return render_template("register.html", form=form, message=message)
    return render_template("register.html", form=form)


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        if not recaptcha.verify():
            return render_template("forgot_password.html", form=form, message="Подтвердите что вы не робот")
        else:
            info = json.loads(requests.get(DOMEN + "/api/users/" + TOKEN).content)['users']
            for i in range(len(info)):
                if info[i]['email'] == form.email.data:
                    password = gen_password()
                    info[i]['hashed_password'] = generate_password_hash(password)
                    send_email_to([info[i]['email']], "Ваш пароль от сайта: {}".format(password))
                    requests.put(DOMEN + "/api/users/" + TOKEN + "/" + str(info[i]['id']),
                                 json=info[i])
                    return render_template("forgot_password.html", form=form, message="ОК")
            return render_template("forgot_password.html", form=form, message="Не найдена почта")
    return render_template("forgot_password.html", form=form)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.hashed_password, form.old_password.data):
            if form.new_password.data == form.rep_password.data:
                info = json.loads(
                    requests.get(DOMEN + "/api/users/" + TOKEN + "/" + str(current_user.id)).content)[
                    'users']
                info['hashed_password'] = generate_password_hash(form.new_password.data)
                requests.put(DOMEN + "/api/users/" + TOKEN + "/" + str(current_user.id), params=info)
                return render_template("settings.html", form=form, message="OK")
            return render_template("settings.html", form=form, message="Пароли не совпадают")
        return render_template("settings.html", form=form, message="Неверный старый пароль")
    return render_template("settings.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/film_page/<int:film_id>", methods=['POST', 'GET'])
def film_page(film_id):
    form = CommentForm()
    info_user = json.loads(requests.get(DOMEN + "/api/users/" + TOKEN).content)['users']
    info_comment = json.loads(requests.get(DOMEN + "/api/comments/" + TOKEN).content)['comments']
    temps = {}
    for i in range(len(info_user)):
        temps[info_user[i]['id']] = info_user[i]
    comments = []
    for i in range(len(info_comment)):
        if info_comment[i]['film_id'] == film_id and info_comment[i]['user_id'] in temps:
            comments.append({'username': temps[info_comment[i]['user_id']]['nickname'],
                             'text': info_comment[i]['text'],
                             'photo_url': temps[info_comment[i]['user_id']]['photo_url'],
                             'id': info_comment[i]['id']})
    film_info = json.loads(requests.get(DOMEN + "/api/films/" + TOKEN + "/" + str(film_id)).content)
    if form.validate_on_submit():
        info = requests.post(DOMEN + "/api/comments/" + TOKEN,
                             json={'film_id': film_id, 'user_id': current_user.id, 'text': form.text.data}).content
        return redirect("/film_page" + "/" + str(film_id))
    return render_template("film_page.html", film=film_info['films'], form=form, comment=comments)


@app.route("/add_film", methods=['GET', 'POST'])
@login_required
def add_film():
    if current_user.access_level < 3:
        return redirect("/")
    form = AddFilmForm()
    if form.validate_on_submit():
        params = {
            'title': form.title.data,
            'year': form.year.data,
            'country': form.country.data,
            'genre': form.genre.data,
            'age': form.age.data,
            'description': form.description.data,
            'show': form.show.data,
            'film_url': form.film_url.data,
            'photo_url': form.photo_url.data,
            'score': form.score.data
        }
        info = json.loads(requests.post(DOMEN + "/api/films/" + TOKEN, json=params).content)
        message = ""
        for key in info:
            message += str(info[key]) + "\n"
        return render_template("add_film.html", form=form, message=message)
    return render_template("add_film.html", form=form)


@app.route("/edit_film/<int:film_id>", methods=['GET', 'POST'])
@login_required
def edit_film(film_id):
    if current_user.access_level < 3:
        return redirect("/")
    info = json.loads(requests.get(DOMEN + "/api/films/" + TOKEN + "/" + str(film_id)).content)['films']
    form = EditFilmForm()
    if form.validate_on_submit():
        print(form.score.data)
        params = {
            'title': form.title.data,
            'year': form.year.data,
            'country': form.country.data,
            'genre': form.genre.data,
            'age': form.age.data,
            'description': form.description.data,
            'show': form.show.data,
            'film_url': form.film_url.data,
            'photo_url': form.photo_url.data,
            'score': form.score.data
        }
        info = json.loads(requests.put(DOMEN + "/api/films/" + TOKEN + "/" + str(film_id), json=params).content)
        message = ""
        for key in info:
            message += str(info[key]) + "\n"
        print(message)
        if message == "OK\n":
            return redirect("/film_page" + "/" + str(film_id))
        return render_template("edit_film.html", form=form, info=info, message=message)
    return render_template("edit_film.html", form=form, info=info)


@app.route("/delete_comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    info = json.loads(requests.get(DOMEN + "/api/comments/" + TOKEN).content)['comments']
    for i in range(len(info)):
        if info[i]['id'] == comment_id:
            if current_user.access_level >= 3 or current_user.id == info[i]['user_id']:
                requests.delete(DOMEN + "/api/comments/" + TOKEN + "/" + str(info[i]['user_id']))
            return redirect("/film_page/{}".format(info[i]['film_id']))


@app.route("/delete_film/<int:film_id>")
@login_required
def delete_film(film_id):
    if current_user.access_level < 3:
        return redirect("/")
    requests.delete(DOMEN + "/api/films/" + TOKEN + "/" + str(film_id))
    return redirect("/")


@app.route("/search", methods=['POST', 'GET'])
def search_web():
    text = request.args.get('search_bar_value')
    info = json.loads(requests.get(DOMEN + "/api/films/" + TOKEN).content)['films']

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    for i in range(len(info)):
        film_info = info[i]['description'] + " " + info[i]['genre'] +\
                    " " + info[i]['age'] + " " + info[i]['country'] + " " + info[i]['title']
        writer.add_document(title=u"{}".format(i), path=u"/a", content = u"{}".format(film_info))
    writer.commit()
    data = []
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(text.replace("+", " "))
        results = searcher.search(query)
        for i in range(len(results)):
            data.append(info[int(results[i]['title'])])
    return render_template("search.html", info=data, text=text.replace("+", " "))


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run()
