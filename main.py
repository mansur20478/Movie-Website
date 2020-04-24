from security.const import SECRET_KEY
from forms.forms import *

from data import db_session
from flask_login import LoginManager
from flask import Flask, render_template
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
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


@app.route("/film_page")
def film_page():
    film_info = {
        'photo_url': 'https://gidonline.io/img/9b85f7218_200x300.jpg',
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


if __name__ == '__main__':
    app.run()
