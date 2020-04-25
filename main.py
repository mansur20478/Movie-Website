from security.const import SECRET_KEY, TOKEN, RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY
from forms.forms import *
from data import db_session
import films_resource

import requests
import json
from flask_recaptcha import ReCaptcha
from flask_restful import Api
from flask_login import LoginManager
from flask import Flask, render_template
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
api = Api(app)
api.add_resource(films_resource.FilmsListResource, '/api/films/<token>')
api.add_resource(films_resource.FilmsResource, '/api/films/<token>/<int:films_id>')
recaptcha = ReCaptcha()
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_SITE_KEY'] = RECAPTCHA_SITE_KEY
app.config['RECAPTCHA_SECRET_KEY'] = RECAPTCHA_SECRET_KEY
recaptcha.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("base.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()


@app.route("/film_page/<int:film_id>")
def film_page(film_id):
    film_info = {
        'photo_url': 'https://upload.wikimedia.org/wikipedia/ru/thumb/9/93/Pulp_Fiction.jpg/211px-Pulp_Fiction.jpg',
        'title': 'title',
        'year': 'year',
        'country': 'country',
        'genre': 'genre',
        'duration': 'duration',
        'description': 'description',
        'score': 10,
        'film_url': 'https://stonehenge.load.hdrezka-ag.net/tvseries/f455776e70b462a514403e5dae056fc894ca5c92/a2b31d7e35a4d1a4bb024721e145d494:2020042511/240.mp4'
    }
    return render_template("film_page.html", film=film_info)


@app.route("/add_film", methods=['GET', 'POST'])
def add_film():
    form = AddFilmForm()
    if form.validate_on_submit() and recaptcha.verify():
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
        info = json.loads(requests.post("http://localhost:5000/api/films/" + TOKEN, json=params).content)
        message = ""
        for key in info:
            message += str(info[key]) + "\n"
        return render_template("add_film.html", form=form, message=message)
    return render_template("add_film.html", form=form)


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run()
