from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired

from datetime import datetime

from crm.event_types import get_event_types


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


class EventsForm(FlaskForm):
    start_date = DateTimeLocalField(
        'Все события с',
        format='%Y-%m-%dT%H:%M',
        default=datetime(2008, 1, 1)
    )
    end_date = DateTimeLocalField(
        'До',
        format='%Y-%m-%dT%H:%M',
        default=datetime(2027, 1, 1)
    )
    event_type = SelectField('Тип событий', choices=[])
    created_by = SelectField('Автор', choices=[("", "ВСЕ"), ("0", "Робот")])

    submit = SubmitField('Вывести')

    def __init__(self, *args, **kwargs):
        print("form init")
        """Запрос к бд для получения всех типов данных"""
        super(EventsForm, self).__init__(*args, **kwargs)
        self.event_type.choices = [('', "ВСЕ")] + [(event.name, event.translation) for event in get_event_types()]
