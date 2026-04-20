from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional

from datetime import datetime


# from utils import get_events_type


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
        default=datetime.now
    )
    event_type = SelectField('Тип событий', choices=[])

    submit = SubmitField('Вывести')

    def set_events_form_choices(self, db_session) -> None:
        """запрос к бд для получения всех типов данных"""
        from src.models.events_type import Events_type
        with db_session.create_session() as db_sess:
            events_name = [event.translation for event in db_sess.query(Events_type).all()]
            self.event_type.choices = [(event_name, event_name) for event_name in events_name]
        return
