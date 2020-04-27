from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddFilmForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    genre = StringField("Genre", validators=[DataRequired()])
    duration = StringField("Duration", validators=[DataRequired()])
    age = StringField("Age restrictions", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    film_url = StringField("Film url", validators=[DataRequired()])
    photo_url = StringField("Photo url", validators=[DataRequired()])
    score = IntegerField("Score(KinoPoisk)", validators=[DataRequired()])
    show = BooleanField("Show")
    submit = SubmitField("Submit")
