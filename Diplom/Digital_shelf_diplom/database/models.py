# Цель: ORM-модели базы данных
# Модели:
# Detection (результаты детекции):

# id - первичный ключ
# photo_path - путь к оригинальному фото
# annotated_photo_path - путь к аннотированному фото
# detection_results - JSON с координатами объектов
# user_id - ID пользователя Telegram
# store_id - FK на магазин
# timestamp - время загрузки
# processing_time - время обработки

# Report (отчёты о соответствии):

# id - первичный ключ
# detection_id - FK на Detection
# compliance_percentage - процент соответствия планограмме
# violations - JSON с нарушениями
# recommendations - рекомендации
# created_at - время создания

# Product (продукты компании):

# id - первичный ключ
# name - название продукта
# category - категория
# sku - артикул
# expected_position - ожидаемая позиция на полке

# Store (магазины):

# id - первичный ключ
# name - название магазина
# address - адрес
# chain - торговая сеть

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base




class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    chain = Column(String)
    
    
class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    photo_path = Column(String, nullable=False)
    annotated_photo_path = Column(String)
    detection_results = Column(JSON)
    user_id = Column(Integer, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)

    store = relationship("Store")
    report = relationship("Report", back_populates="detection", uselist=False)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    detection_id = Column(Integer, ForeignKey("detections.id"))
    compliance_percentage = Column(Float)
    violations = Column(JSON)
    recommendations = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    detection = relationship("Detection", back_populates="report")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)
    sku = Column(String)
    expected_position = Column(String)
