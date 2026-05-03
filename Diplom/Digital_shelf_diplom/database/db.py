# Цель: Настройка подключения к БД
# Методы:

# init_db() - инициализация БД (создание таблиц)
# get_engine() - получение SQLAlchemy engine
# get_session() - фабрика сессий
# async_session_maker() - асинхронные сессии (если используется asyncio)
# database/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db"
Base = declarative_base()

_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    return _engine

def get_session():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal()

def init_db():
    # КРИТИЧЕСКИЙ МОМЕНТ: импортируем модели здесь, чтобы Base их "увидел"
    import database.models 
    engine = get_engine()
    Base.metadata.create_all(bind=engine)