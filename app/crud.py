# app/crud.py
from sqlalchemy.orm import Session
from . import models

def get_organization(db: Session, org_id: int):
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

def get_organizations_by_building(db: Session, building_id: int):
    return db.query(models.Organization).filter(models.Organization.building_id == building_id).all()

def get_organizations_by_activity(db: Session, activity_ids: list):
    # Выборка организаций, у которых хотя бы одна деятельность из заданного списка
    return db.query(models.Organization)\
             .join(models.Organization.activities)\
             .filter(models.Activity.id.in_(activity_ids)).all()

def get_organizations_by_name(db: Session, name: str):
    # Поиск по названию (без учёта регистра, частичное совпадение)
    return db.query(models.Organization).filter(models.Organization.name.ilike(f"%{name}%")).all()

def get_activity_by_name(db: Session, activity_name: str):
    return db.query(models.Activity).filter(models.Activity.name == activity_name).first()

def get_activity_by_id(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()

# def get_child_activity_ids(activity: models.Activity):
#     """
#     Рекурсивно собираем идентификаторы активности и всех её дочерних элементов.
#     """
#     ids = [activity.id]
#     for child in activity.children:
#         ids.extend(get_child_activity_ids(child))
#     return ids
