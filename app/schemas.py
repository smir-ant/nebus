from typing import List, Optional
from pydantic import BaseModel, validator

class Building(BaseModel):
    address: str
    latitude: float
    longitude: float
    id: int

# class Building(BuildingBase):
    

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class Activity(ActivityBase):
    id: int
    children: List["Activity"] = []

    @validator("children", pre=True, always=True)
    def set_children(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return [v]

class OrganizationBase(BaseModel):
    name: str
    phone_numbers: List[str]
    building_id: int

class Organization(OrganizationBase):
    id: int
    building: Building
    activities: List[Activity] = []

    # Валидатор для преобразования строки номеров телефонов в список
    @validator("phone_numbers", pre=True)
    def split_phone_numbers(cls, v):
        if isinstance(v, str):
            return [phone.strip() for phone in v.split(",")]
        return v

# схемы для ответа эндпоинта "найти организации в радиусе"
class OrganizationSimple(BaseModel):
    id: int
    name: str
    phone_numbers: List[str]

class BuildingWithOrganizations(Building):
    organizations: List[OrganizationSimple] = []

    # Если в базе организаций нет, всегда возвращаем пустой список
    @validator("organizations", pre=True, always=True)
    def set_organizations(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return [v]

# Обновляем ссылки для рекурсивной схемы
Activity.update_forward_refs()
