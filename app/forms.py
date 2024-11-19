from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# Импортируем модуль User из нашего модуля
from app.models import User


# Создаём класс RegistrationForm для регистрации, который будет создавать форму:
class RegistrationForm(FlaskForm):
    # создаем 4 поля и 1 кнопку
    # валидатор проверяет условия из []
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Повторение пароля. Валидатор будет сравнивать пароли
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Создаём функции для проверки уникальности имени пользователя и почты:
    def validate_username(self, username):
        # класс User с БД.
        # Будет искать первое совпадающее имя
        user = User.query.filter_by(username=username.data).first()
        # Если такой юзер все-таки найдется, то ошибка:
        # raise - генератор исключения
        if user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такая почта уже используется')


# Создание класса LoginForm для логинирования
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')
