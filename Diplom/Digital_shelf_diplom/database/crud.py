# Цель: CRUD-операции с базой данных
# Классы и методы:
# DetectionCRUD:

# create_detection(photo_path, results, user_id) - сохранение результата детекции
# get_detection_by_id(detection_id) - получение детекции по ID
# get_detections_by_date(start_date, end_date) - выборка за период
# get_detections_by_store(store_id) - детекции по магазину
# update_detection_status(detection_id, status) - обновление статуса

# ReportCRUD:

# create_report(detection_id, compliance_score, violations) - создание отчёта
# get_report_by_id(report_id) - получение отчёта
# get_reports_summary(start_date, end_date) - сводка по отчётам
# calculate_average_compliance(period) - средний процент соответствия

# ProductCRUD:

# get_all_products() - список всех продуктов компании
# get_product_by_name(name) - поиск продукта по названию

from sqlalchemy.orm import Session
from .models import Detection, Report, Product
from datetime import datetime


class DetectionCRUD:

    @staticmethod
    def create_detection(db: Session, photo_path, results, user_id, store_id=None, processing_time=None):
        detection = Detection(
            photo_path=photo_path,
            detection_results=results,
            user_id=user_id,
            store_id=store_id,
            processing_time=processing_time
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)
        return detection

    @staticmethod
    def get_detection_by_id(db: Session, detection_id):
        return db.query(Detection).filter(Detection.id == detection_id).first()

    @staticmethod
    def get_detections_by_date(db: Session, start_date, end_date):
        return db.query(Detection).filter(
            Detection.timestamp >= start_date,
            Detection.timestamp <= end_date
        ).all()

    @staticmethod
    def get_detections_by_store(db: Session, store_id):
        return db.query(Detection).filter(Detection.store_id == store_id).all()

    @staticmethod
    def update_detection_status(db: Session, detection_id, annotated_path):
        detection = db.query(Detection).filter(Detection.id == detection_id).first()
        if detection:
            detection.annotated_photo_path = annotated_path
            db.commit()
            db.refresh(detection)
        return detection
    

class ReportCRUD:

    @staticmethod
    def create_report(db: Session, detection_id, compliance_score, violations, recommendations=""):
        report = Report(
            detection_id=detection_id,
            compliance_percentage=compliance_score,
            violations=violations,
            recommendations=recommendations
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_report_by_id(db: Session, report_id):
        return db.query(Report).filter(Report.id == report_id).first()

    @staticmethod
    def get_reports_summary(db: Session, start_date, end_date):
        reports = db.query(Report).filter(
            Report.created_at >= start_date,
            Report.created_at <= end_date
        ).all()

        return [
            {
                "id": r.id,
                "compliance": r.compliance_percentage,
                "date": r.created_at
            }
            for r in reports
        ]

    @staticmethod
    def calculate_average_compliance(db: Session, start_date, end_date):
        reports = db.query(Report).filter(
            Report.created_at >= start_date,
            Report.created_at <= end_date
        ).all()

        if not reports:
            return 0

        avg = sum(r.compliance_percentage for r in reports) / len(reports)
        return avg
    
    
class ProductCRUD:

    @staticmethod
    def get_all_products(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product_by_name(db: Session, name):
        return db.query(Product).filter(Product.name == name).first()
    