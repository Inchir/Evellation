from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Optional

from datetime import datetime


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


class DataForm(FlaskForm):
    start_date = DateField('Все события с', format='%Y-%m-%d',
                           validators=[DataRequired()],
                           default=datetime.now)
    end_date = DateField('До', format='%Y-%m-%d',
                         validators=[DataRequired()],
                         default=datetime.now)
    data_type = StringField('Тип событий', validators=[Optional()])

    submit = SubmitField('Вывести')
