import asyncio
from sqlalchemy import (Column, insert, Integer,
                        select, String, Text, update)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    days = Column(Integer, default=3)
    login = Column(String(40), unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    text = Column(Text)

    def __repr__(self):
        return (f'Ваш Телеграм ID: {self.tg_id}\n'
                f'Имя в Телеграм: {self.login}\n'
                f'Почта:{self.login}\n'
                f'Пароль:{self.password}\n'
                f'Дней отслеживания:{self.days}')

# engine = create_engine('sqlite:///./sqlite.db', echo=False)
# Base.metadata.drop_all(engine)  # Удаление таблицы


engine = create_async_engine('sqlite+aiosqlite:///./sqlite.db', echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Запуск асинхронного создания таблиц
asyncio.run(init_db())
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
# session.add(user3)
# session.add(user4)
# session.add(user5)

# session.commit()


async def get_user_by_tg_id(tg_id: int):
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user if user else None


# async def main():
#     user_data = await get_user_by_tg_id(5583668411)
#     print(user_data.login)

user = asyncio.run(get_user_by_tg_id(5583668411))
print(user.id)
