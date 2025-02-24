from sqlalchemy import (create_engine, Column, insert, Integer,
                        select, String, Text)
from sqlalchemy.orm import Session, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    days = Column(Integer, default=3)
    name = Column(String(40))
    login = Column(String(40), nullable=False)
    password = Column(String(40), nullable=False)
    text = Column(Text)

    def __repr__(self):
        return (f'Ваш Телеграм ID: {self.tg_id}\n'
                f'Имя в Телеграм: {self.login}\n'
                f'Почта:{self.login}\n'
                f'Пароль:{self.password}\n'
                f'Дней отслеживания:{self.days}')


engine = create_engine('sqlite:///sqlite.db', echo=False)
# Base.metadata.drop_all(engine)  # Удаление таблицы
Base.metadata.create_all(engine)
session = Session(engine)

# session.add(user1)
# session.add(user2)
# session.add(user3)
# session.add(user4)
# session.add(user5)
# session.add(user6)


# session.commit()


def get_user(tg_id):
    call = session.execute(
        select(User).where(User.tg_id == tg_id)
    )
    user = call.scalars().first()
    return user


def add_user(tg_id, name, login, password, days):
    print('add_user')
    if not get_user(tg_id):
        print('not exists')
        session.execute(
            insert(User).values(
                tg_id=tg_id,
                name=name,
                login=login,
                password=password,
                days=days))
        session.commit()
        print('sucsess insertion')


def update_day(tg_id, days):
    print('update_day')
    user = get_user(tg_id)
    if user:
        user.days = days
        session.commit()
        print('sucsess days changes')


def add_schedule_to_db(tg_id, text):
    # print('add_schedule_to_db')
    user = get_user(tg_id)
    if user:
        user.text = text
        session.commit()


def get_schedule_from_db(tg_id):
    print('get_schedule_from_db')
    user = get_user(tg_id)
    if user:
        schedule_from_db = user.text
        print('get text or db')
        return schedule_from_db


def get_all_users():
    users = session.scalars(select(User)).all()
    return users
