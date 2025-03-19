import math
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Тестовое by smir-ant")

# Статический API ключ для всех запросов
API_KEY = "secret"

def get_db():
    """
    Зависимость для получения сессии БД.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_api_key(x_api_key: str = Header(...)):
    """
    Зависимость для проверки API ключа.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Неверный API ключ")
    return x_api_key

# Функция для расчета расстояния по формуле Haversine (в километрах)
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    # градусы -> радианы
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # дельты
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2  # формула эта Гаверсина
    c = 2 * math.asin(math.sqrt(a))  # центральный угол в радианах 
    # p.s. не шарю в геодезии и геометрии не гений, так что мне подсказал интернет формулу, будем считать что она верна
    km = 6371 * c  # 6371 - ср. радиус земли
    return km

@app.get("/organizations/by_building/{building_id}", response_model=List[schemas.Organization],
         dependencies=[Depends(verify_api_key)])
def organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    """
    Эндпоинт возвращает список организаций, находящихся в указанном здании.
    """
    orgs = crud.get_organizations_by_building(db, building_id)
    return orgs

@app.get("/organizations/by_activity/{activity_id}", response_model=List[schemas.Organization],
         dependencies=[Depends(verify_api_key)])
def organizations_by_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Эндпоинт возвращает список организаций по указанному виду деятельности.
    """
    activity = crud.get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Деятельность не найдена")
    orgs = crud.get_organizations_by_activity(db, [activity.id])
    return orgs

@app.get("/organizations/id/{org_id}", response_model=schemas.Organization,
         dependencies=[Depends(verify_api_key)])
def get_organization(org_id: int, db: Session = Depends(get_db)):
    """
    Эндпоинт возвращает данные организации по её идентификатору.
    """
    org = crud.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return org

@app.get("/organizations/search", response_model=List[schemas.Organization],
         dependencies=[Depends(verify_api_key)])
def search_organizations(name: str = None, db: Session = Depends(get_db)):
    """
    Эндпоинт для поиска организаций по названию (частичное совпадение).
    Чувствителен к регистру.
    """
    orgs = crud.get_organizations_by_name(db, name)
    return orgs

@app.get("/organizations/search_by_activity", response_model=List[schemas.Organization],
         dependencies=[Depends(verify_api_key)])
def search_organizations_by_activity(activity: str = None,db: Session = Depends(get_db)):
    """
    Эндпоинт для поиска организаций по виду деятельности(str, не id).
    """
    act = crud.get_activity_by_name(db, activity)
    if not act:
        raise HTTPException(status_code=404, detail="Деятельность не найдена")
    activity_ids = act.id
    orgs = crud.get_organizations_by_activity(db, activity_ids)
    return orgs

# поскольку работать с геодезическими форматами-данными можно более ловко, но будто лишнее фигачить для тестового, 
# то взят перебор всех зданий и высчитывание расстояние меж точкой и зданием
@app.get("/organizations/nearby", response_model=List[schemas.BuildingWithOrganizations],
         dependencies=[Depends(verify_api_key)])
def organizations_nearby(lat: float, lon: float, radius: float, db: Session = Depends(get_db)):
    """
    Возвращает список зданий и организаций в них, которые находятся в заданном радиусе (в км)
    от указанной точки (lat, lon).
    """
    buildings = db.query(models.Building).all()
    nearby_buildings = []
    for building in buildings:
        # Вычисляем расстояние между заданной точкой и зданием
        distance = haversine(lon, lat, building.longitude, building.latitude)
        if distance <= radius:
            nearby_buildings.append(building)
    return nearby_buildings