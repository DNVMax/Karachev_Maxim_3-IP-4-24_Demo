import os
from sqlalchemy import *
from sqlalchemy.orm import *

# Получаем абсолютный путь к папке, где лежит этот файл (py/), 
# и указываем путь к app.db на уровень выше или прямо здесь же.
# Давай положим app.db прямо рядом с app.py / models.py:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String)
    is_locked = Column(Integer, nullable=False, default=0)
    attempts = Column(Integer, nullable=False, default=0)

# Автоматически создадим таблицы, если их нет, чтобы не было ошибок отражения
Base.metadata.create_all(engine)

def _to_dict(user):
    if user is None:
        return None
    return {
        "id": user.id,
        "login": user.login,
        "password": user.password,
        "role": user.role,
        "full_name": user.full_name,
        "locked": bool(user.is_locked),
        "attempts": user.attempts,
    }

def all_users():
    with Session(engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [_to_dict(u) for u in users]

def find_user(login, password):
    with Session(engine) as session:
        user = session.scalars(
            select(User).where(User.login == login, User.password == password)
        ).first()
        return _to_dict(user)

def user_by_login(login):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.login == login)).first()
        return _to_dict(user)

def login_exists(login):
    return user_by_login(login) is not None

def add_user(login, password, role, full_name):
    with Session(engine) as session:
        session.add(
            User(
                login=login,
                password=password,
                full_name=full_name,
                role=role,
                is_locked=0,
                attempts=0,
            )
        )
        session.commit()

def update_user(login, password, role, full_name):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.login == login)).first()
        if user is None:
            return False
        user.password = password
        user.role = role
        user.full_name = full_name
        session.commit()
        return True

def delete_user(login):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.login == login)).first()
        if user is None:
            return False
        session.delete(user)
        session.commit()
        return True

def register_fail(login):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.login == login)).first()
        if user is None:
            return False
        user.attempts = user.attempts + 1
        if user.attempts >= 3:
            user.is_locked = 1
        session.commit()
        return True

def reset_attempts(login):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.login == login)).first()
        if user is None:
            return False
        user.attempts = 0
        session.commit()
        return True

def unlock_user(login):
    with Session(engine) as session:
        user = session.scalars(select(User).where(User.login == login)).first()
        if user is None:
            return False
        user.is_locked = 0
        user.attempts = 0
        session.commit()
        return True

if __name__ == "__main__":
    for user in all_users():
        print(user)