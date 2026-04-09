from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Создать аккаунт')


class AccountForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    subdomain = StringField('Субдомен', validators=[DataRequired()])
    submit = SubmitField('Добавить аккаунт')


class TokenForm(FlaskForm):
    token = StringField('Ключ', validators=[DataRequired()])
    submit = SubmitField('Введите')

