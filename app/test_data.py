from .database import SessionLocal, engine, Base
from . import models

def create_and_populate_test_data():
    """
    Создания таблиц (если они ещё не существуют) и наполнения бд тестовыми данными.
    Это упрощённый вариант для локальной разработки.
    """
    # Создаем таблицы, если они не существуют (метод create_all является идемпотентным)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Опциональная очистка таблиц (если требуется начать с чистой базы)
    db.query(models.Organization).delete()
    db.query(models.Activity).delete()
    db.query(models.Building).delete()
    db.commit()
    
    # Создаем здания
    building1 = models.Building(address="г. Москва, ул. Прикольная 1, офис 3", latitude=55.555, longitude=33.333)
    building2 = models.Building(address="г. Москва, ул. Балдёжная 2", latitude=56.5656, longitude=30.3030)
    db.add_all([building1, building2])
    db.commit()
    
    # Создаём виды деятельности (пример древовидной структуры)
    food = models.Activity(name="Еда")
    meat = models.Activity(name="Мясная продукция", parent=food)
    milk = models.Activity(name="Молочная продукция", parent=food)
    
    cars = models.Activity(name="Автомобили")
    # imho: реализовал под копирку с тестового, и поэтому запчасти+аксессуары только легковушкам
    trucks = models.Activity(name="Грузовые", parent=cars)
    legkovie = models.Activity(name="Легковые", parent=cars)
    zapchasti = models.Activity(name="Запчасти", parent=legkovie)
    accessories = models.Activity(name="Аксессуары", parent=legkovie)
    
    db.add_all([food, meat, milk, cars, trucks, legkovie, zapchasti, accessories])
    db.commit()
    
    # Создаём организации и связываем с соответствующими зданиями и видами деятельности
    org1 = models.Organization(
        name="ООО Рога и Копыта",
        phone_numbers="2-222-222,3-333-333",
        building_id=building1.id
    )
    org1.activities.extend([food, meat])
    
    org2 = models.Organization(
        name="ЗАО Бещеки",
        phone_numbers="8-923-666-13-13",
        building_id=building1.id
    )
    org2.activities.append(meat)
    
    org3 = models.Organization(
        name="ООО АвтоМир",
        phone_numbers="4-444-444",
        building_id=building2.id
    )
    org3.activities.extend([cars, legkovie])
    
    db.add_all([org1, org2, org3])
    db.commit()
    db.close()

if __name__ == "__main__":
    create_and_populate_test_data()




# ---------------------

# from .database import SessionLocal
# from . import models

# def create_test_data():
#     db = SessionLocal()
#     # Очистка таблиц (для теста)
#     db.query(models.Organization).delete()
#     db.query(models.Activity).delete()
#     db.query(models.Building).delete()
#     db.commit()
    
#     # Создаём здания
#     building1 = models.Building(address="г. Москва, ул. Прикольная 1, офис 3", latitude=55.555, longitude=33.333)
#     building2 = models.Building(address="г. Москва, ул. Балдёжная 2", latitude=56.5656, longitude=30.3030)
#     db.add_all([building1, building2])
#     db.commit()
    
#     # Создаём виды деятельности (пример древовидной структуры)
#     food = models.Activity(name="Еда")
#     meat = models.Activity(name="Мясная продукция", parent=food)
#     milk = models.Activity(name="Молочная продукция", parent=food)
    
#     cars = models.Activity(name="Автомобили")
#     # imho: реализовал под копирку с тестового, и поэтому запчасти+аксессуары только легковушкам
#     trucks = models.Activity(name="Грузовые", parent=cars)
#     legkovie = models.Activity(name="Легковые", parent=cars)
#     zapchasti = models.Activity(name="Запчасти", parent=legkovie)
#     accessories = models.Activity(name="Аксессуары", parent=legkovie)
    
#     db.add_all([food, meat, milk, cars, trucks, legkovie, zapchasti, accessories])
#     db.commit()
    
#     # Создаём организации и связываем с соответствующими зданиями и видами деятельности
#     org1 = models.Organization(
#         name="ООО Рога и Копыта",
#         phone_numbers="2-222-222,3-333-333",
#         building_id=building1.id
#     )
#     org1.activities.extend([food, meat])
    
#     org2 = models.Organization(
#         name="ЗАО Бещеки",
#         phone_numbers="8-923-666-13-13",
#         building_id=building1.id
#     )
#     org2.activities.append(meat)
    
#     org3 = models.Organization(
#         name="ООО АвтоМир",
#         phone_numbers="4-444-444",
#         building_id=building2.id
#     )
#     org3.activities.extend([cars, legkovie])
    
#     db.add_all([org1, org2, org3])
#     db.commit()
#     db.close()

# if __name__ == "__main__":
#     create_test_data()
