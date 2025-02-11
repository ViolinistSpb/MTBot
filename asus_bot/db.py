from sqlalchemy import (create_engine, Column, insert, Integer,
                        select, String, Text, update)
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    days = Column(Integer, default=3)
    name = Column(String(40))
    login = Column(String(40), unique=True, nullable=False)
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

# user1 = User(
#     tg_id=1054725325,
#     days=3,
#     login='malkov@mariinsky.ru',
#     password='0t4=9x2E%1Yw'
# )

user2 = User(
    tg_id=542521964,
    days=2,
    login='lan',
    password='vitaly_pugachev13.11.1989',
    text='schedule'
)

user3 = User(
    tg_id=345736727,
    days=3,
    login='serebro',
    password='LeR4#K$6f25u'
)

user4 = User(
    tg_id=266159638,
    days=3,
    login='gribanova@mariinsky',
    password='?NILqW39=Hut'
)

user5 = User(
    tg_id=5583668411,
    days=3,
    login='Goncharov_kg@mariinsky.ru',
    password='b1*C&0Zsv6YU'
)

# session.add(user2)
# session.commit()
# session.add(user3)
# session.add(user4)
# session.add(user5)

# session.commit()


def check_user_exists(tg_id):
    print('check_user_exists')
    call = session.execute(
        select(User).where(User.tg_id == tg_id)
    )
    user = call.scalars().first()
    return True if user else False


def add_or_update_user(tg_id, name, login, password, days):
    print('add_or_update_user')
    if check_user_exists(tg_id):
        print('exists, trying to change user')
        session.execute(
            update(User).where(User.tg_id == tg_id).values(
                tg_id=tg_id,
                name=name,
                login=login,
                password=password,
                days=days))
        session.commit()
    else:
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


def update_user(tg_id, name, login, password, days):
    print('update user')
    if check_user_exists(tg_id):
        print('exists, trying to change user')
        session.execute(
            update(User).where(User.tg_id == tg_id).values(
                name=name,
                login=login,
                password=password,
                days=days
            )
        )
        session.commit()
        print('sucsess updation')
        return 


# print(check_user_exists(542521964))
