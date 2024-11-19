# UserMixin Этот класс даёт возможность работать с пользователем
from flask_login import UserMixin

from app import db, login_manager


# декоратор, который сообщает Flask, что функция будет
# использоваться для загрузки пользователя по его ID
@login_manager.user_loader
def load_user(user_id):
    # Эта строчка будет отправлять в БД запрос для поиска
    # определённого юзера по его ID
    return User.query.get(int(user_id))


# Создаём класс User
class User(db.Model, UserMixin):
    # Столбцы в БД
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Функция, чтобы представить информацию о пользователе
    # в виде одной строки
    def __repr__(self):
        return f'User: {self.username}, email: {self.email}'
