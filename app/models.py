# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()



Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    rides = relationship("Ride", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Driver(Base):
    __tablename__ = "drivers"
    driver_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicles = relationship("Vehicle", back_populates="driver")
    rides = relationship("Ride", back_populates="driver")
    ratings = relationship("Rating", back_populates="driver")


class Vehicle(Base):
    __tablename__ = "vehicles"
    vehicle_id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    plate_number = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    type = Column(String, nullable=False)

    driver = relationship("Driver", back_populates="vehicles")


class Ride(Base):
    __tablename__ = "rides"
    ride_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    pickup_location = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    status = Column(String, default="requested")
    requested_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="rides")
    driver = relationship("Driver", back_populates="rides")
    payment = relationship("Payment", uselist=False, back_populates="ride")
    rating = relationship("Rating", uselist=False, back_populates="ride")


class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.ride_id"))
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    status = Column(String, default="pending")
    paid_at = Column(DateTime)

    ride = relationship("Ride", back_populates="payment")


class Rating(Base):
    __tablename__ = "ratings"
    rating_id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.ride_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    rating = Column(Integer, nullable=False)
    comments = Column(String)

    ride = relationship("Ride", back_populates="rating")
    user = relationship("User", back_populates="ratings")
    driver = relationship("Driver", back_populates="ratings")

