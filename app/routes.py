from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User


# Создаём маршрут для главной страницы.
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# Создаём маршрут для страницы регистрации,
# обрабатываем методы GET и POST.
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Проверка: прошел ли пользватель аутентификацию,
    # те есть ли он в системе
    # Если да то:
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Если нет, то отправляем к форме регистрации:
    form = RegistrationForm()
    if form.validate_on_submit():
        # Кодировка пароля
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Создаем объект класса User, туда деваем информацию при регистрации
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Добавление пользователя в сессию и запись в БД
        db.session.add(user)
        db.session.commit()
        # сообщение
        flash('Вы успешно зарегистрировались!', 'success')
        # после регистрации переадресование пользователя
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


# Создаём маршрут для страницы входа,
# также обрабатываем методы GET и POST.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # Проверка, толчно ли нажата кнопка
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # если пароль,который ввели и то, то есть в БД одинаковые, то
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # то логиним юзера
            # учитывая значок из forms.py "запоминать юзера" или нет
            login_user(user, remember=form.remember.data)
            # перенаправление на страницу
            return redirect(url_for('home'))
        # если что-то не верное
        else:
            flash('Введены неверные данные')
    return render_template('login.html', form=form, title='Login')


# Создаём маршрут для выхода из аккаунта.
@app.route('/logout')
def logout():
    logout_user()
    # перенаправление на страницу
    return redirect(url_for('home'))


# Создаём маршрут для отображения страницы аккаунта.
# Декоратор login_required требует, чтобы пользователь был авторизирован.
@app.route('/account')
@login_required
def account():
    return render_template('account.html')
