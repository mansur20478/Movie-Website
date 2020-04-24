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


@app.route("/film_page")
def film_page():
    return render_template("film_page.html")


if __name__ == '__main__':
    app.run()
