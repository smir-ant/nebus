from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from .database import Base

# Таблица-связка для отношения многие ко многим между Организациями и Деятельностями
organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class Building(Base):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    organizations = relationship("Organization", back_populates="building")

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('activities.id'), nullable=True)

    # Определяем самоссылочную связь для древовидной структуры:
    # связь "children" — список дочерних активностей,
    # обратная связь "parent" — скалярная (одиночный родитель) благодаря uselist=False.
    children = relationship(
        "Activity",
        backref=backref("parent", uselist=False),
        remote_side=[id]
    )

    organizations = relationship("Organization", secondary=organization_activity, back_populates="activities")

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_numbers = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'))

    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity, back_populates="organizations")
