from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Interval, Text, CheckConstraint, LargeBinary, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.expression import text
from .database import Base  
from enum import Enum as PyEnum
from sqlalchemy import Enum

class MethodOfApplication(PyEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    FOR_MIXING = "for mixing"

class MedicineKind(PyEnum):
    PILLS = 'pills',
    MIXTURE = 'mixture', 
    OINTMENT = 'ointment', 
    SOLUTION = 'solution', 
    TINCTURE = 'tincture', 
    POWDER = 'powder'

class UnitsOfMeasure(PyEnum):
    GRAMMS = 'g',
    MILLIGRAMS = 'mg', 
    MILLILITERS = 'ml', 
    PIECES = 'pc'


class OrderStatus(PyEnum):
    WAITING = 'waiting for a delivery',
    PRODUCING = 'producing',
    READY = 'ready',
    ISSUEED = 'issued', 
    CANCELLED = 'cancelled'

class MedicineType(PyEnum):
    FINISHED = 'finished',
    MANUFACTURED = 'manufactured'

class Medication(Base):
    __tablename__ = "medication"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    critical_norm = Column(Numeric(10, 2), nullable=False)
    shelf_life = Column(Interval, nullable=False)
    unit_of_measure = Column(Enum(UnitsOfMeasure, name="units_of_measure"),
                             nullable=False)
    units_per_package = Column(Numeric(10, 2), 
                               CheckConstraint('units_per_package > 0', name='medication_units_per_package_check'))
    price = Column(Numeric(10, 2), 
                   CheckConstraint('price > 0', name='medication_price_check'))
    storage_conditions = Column(String(250), nullable=False), 
    current_amount = Column(Numeric(10, 2), 
                            CheckConstraint('current_amount >= 0', name='medication_current_amount_check'))
    
    deliveries = relationship("StockDelivery", back_populates="medication",
        cascade="all, delete-orphan")
    compositions = relationship("Composition", back_populates="medicine")

class Ingredient(Base):
    __tablename__ = "ingredient"

    type = Column(String(100), nullable=False)
    caution = Column(Text, nullable=False)
    incompatibillity = Column(String(250))

    @declared_attr
    def __table_args__(cls):
        return {'postgresql_inherits': 'medication'}
    
    @declared_attr
    def id(cls):
        return Column(Integer, ForeignKey('medication.id'), primary_key=True)
    
    used_in_medicines = relationship("Composition", back_populates="ingredient")

class Medicine(Base):
    __tablename__ = "medicine"

    type = Column(Enum(MedicineType, name="medicine_type"),
                             nullable=False)
    kind = Column(Enum(MedicineKind, name="medicine_kind"),
                             nullable=False)
    application = Column(Enum(MethodOfApplication, name="method_of_application"),
                             nullable=False)
    tech_prep_id = Column(Integer, ForeignKey('technology_of_preparation.id'), nullable=False)

    technology = relationship("Technology", back_populates="medicines")
    prescriptions = relationship("Prescription", back_populates="medicine")

    __table_args__ = (CheckConstraint('tech_prep_id > 0', name='valid_tech_prep'))

    @declared_attr
    def __table_args__(cls):
        return {'postgresql_inherits': 'medication'}
    
    @declared_attr
    def id(cls):
        return Column(Integer, ForeignKey('medication.id'), primary_key=True)

class Composition(Base):
    __tablename__ = "composition"
    
    medicine_id = Column(Integer, ForeignKey('medicine.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)
    
    medicine = relationship("Medicine", back_populates="compositions")
    ingredient = relationship("Ingredient", back_populates="used_in_medicines")

class Technology(Base):
    __tablename__ = "technology_of_preparation"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    medicines = relationship("Medicine", back_populates="technology")

class Prescription(Base):
    __tablename__ = "prescription"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey('medicine.id'), nullable=False)
    prescription_number = Column(Integer,
        CheckConstraint('prescription_number > 0', name='prescription_prescription_number_check'),
        nullable=False)
    doctor_surname = Column(String(50), nullable=False)
    doctor_name = Column(String(50), nullable=False)
    doctor_patronymic = Column(String(50))
    signature = Column(LargeBinary, nullable=False)
    stamp = Column(LargeBinary, nullable=False)
    age = Column(Integer,
        CheckConstraint('age >= 0', name='prescription_age_check'),
        nullable=False)
    diagnosis = Column(String(100), nullable=False)
    ammount = Column(Numeric(10, 2),
        CheckConstraint('ammount > 0', name='prescription_ammount_check'), 
        nullable=False)
    application = Column(String(100), nullable=False)

    medicine = relationship("Medicine", back_populates="prescriptions")
    
class Order(Base):
    __tablename__ = "medicine_order"

    id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer, ForeignKey('prescription.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    order_number = Column(Integer,
        CheckConstraint('order_number > 0', name='medicine_order_order_number_check'),
        nullable=False)
    order_date = Column(Date,
        CheckConstraint('order_date <= CURRENT_DATE', name='medicine_order_order_date_check'),
        nullable=False,
        server_default=text('CURRENT_DATE')
    )
    status = Column(Enum(OrderStatus, name="order_status"), nullable=False)
    date_of_issue = Column(Date,
        CheckConstraint(
            'date_of_issue IS NULL OR date_of_issue <= CURRENT_DATE',
            name='medicine_order_date_of_issue_check'
        )
    )
    production_time = Column(Interval,
        CheckConstraint('production_time >= 0', name='medicine_order_production_time_check')
    )
    cost = Column(
        Numeric(10, 2),
        CheckConstraint('cost > 0', name='medicine_order_cost_check'),
        nullable=False
    )

    prescription = relationship("Prescription", back_populates="orders")
    client = relationship("Client", back_populates="orders")


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    phone_number = Column(String(15), nullable=False)

    orders = relationship("Order", back_populates="client")

class StockDelivery(Base):
    __tablename__ = "medication_delivery"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, 
        ForeignKey('medication.id', ondelete='RESTRICT'), 
        nullable=False)
    application_date = Column(Date,
        CheckConstraint('application_date <= CURRENT_DATE', name='medication_delivery_application_date_check'),
        nullable=False, server_default=text('CURRENT_DATE'))
    delivery_date = Column(Date,
        CheckConstraint(
            'delivery_date IS NULL OR delivery_date <= CURRENT_DATE',
            name='medication_delivery_delivery_date_check'
        )
    )
    amount = Column(Numeric(10, 2),
        CheckConstraint('amount > 0', name='medication_delivery_amount_check'),
        nullable=False)

    medication = relationship("Medication", back_populates="deliveries")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(
        Integer, 
        ForeignKey('medication.id', ondelete='RESTRICT'), 
        nullable=False
    )
    date = Column(
        Date,
        CheckConstraint('date <= CURRENT_DATE', name='inventory_date_check'),
        nullable=False,
        server_default=text('CURRENT_DATE')  # Значение по умолчанию - текущая дата
    )
    amount = Column(
        Integer,
        CheckConstraint('amount >= 0', name='inventory_amount_check'),
        nullable=False
    )

    medication = relationship("Medication", back_populates="inventory_records")