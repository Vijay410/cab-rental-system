"""add tables for cab rental system

Revision ID: 3bcc691b66e3
Revises: e6a89809adeb
Create Date: 2025-09-20 20:09:54.289002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bcc691b66e3'
down_revision: Union[str, Sequence[str], None] = 'e6a89809adeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
    '''
    CREATE SEQUENCE "users_user_id_seq" START 1;
    CREATE TABLE "users"(
    user_id INTEGER  PRIMARY KEY DEFAULT nextval('"users_user_id_seq"'),
    name VARCHAR,
    email VARCHAR UNIQUE NOT NULL,
    phone VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE SEQUENCE drivers_driver_id_seq START 1;

    CREATE TABLE drivers (
        driver_id INT PRIMARY KEY DEFAULT nextval('drivers_driver_id_seq'),
        name VARCHAR NOT NULL,
        license_number VARCHAR UNIQUE NOT NULL,
        phone VARCHAR UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


    -- ==========================
    -- Vehicles Table
    -- ==========================
    CREATE SEQUENCE vehicles_vehicle_id_seq START 1;

    CREATE TABLE vehicles (
        vehicle_id INT PRIMARY KEY DEFAULT nextval('vehicles_vehicle_id_seq'),
        driver_id INT NOT NULL,
        plate_number VARCHAR UNIQUE NOT NULL,
        model VARCHAR NOT NULL,
        type VARCHAR NOT NULL,
        CONSTRAINT fk_vehicle_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE
    );


    -- Rides Table
    -- ==========================
    CREATE SEQUENCE rides_ride_id_seq START 1;

    CREATE TABLE rides (
        ride_id INT PRIMARY KEY DEFAULT nextval('rides_ride_id_seq'),
        user_id INT NOT NULL,
        driver_id INT NOT NULL,
        pickup_location VARCHAR NOT NULL,
        dropoff_location VARCHAR NOT NULL,
        status VARCHAR DEFAULT 'requested',
        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        CONSTRAINT fk_ride_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        CONSTRAINT fk_ride_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE
    );


    -- ==========================
    -- Payments Table
    -- ==========================
    CREATE SEQUENCE payments_payment_id_seq START 1;

    CREATE TABLE payments (
        payment_id INT PRIMARY KEY DEFAULT nextval('payments_payment_id_seq'),
        ride_id INT UNIQUE NOT NULL,
        amount FLOAT NOT NULL,
        method VARCHAR NOT NULL,
        status VARCHAR DEFAULT 'pending',
        paid_at TIMESTAMP,
        CONSTRAINT fk_payment_ride FOREIGN KEY (ride_id) REFERENCES rides(ride_id) ON DELETE CASCADE
    );

    -- ==========================
    CREATE SEQUENCE ratings_rating_id_seq START 1;

    CREATE TABLE ratings (
        rating_id INT PRIMARY KEY DEFAULT nextval('ratings_rating_id_seq'),
        ride_id INT UNIQUE NOT NULL,
        user_id INT NOT NULL,
        driver_id INT NOT NULL,
        rating INT NOT NULL,
        comments VARCHAR,
        CONSTRAINT fk_rating_ride FOREIGN KEY (ride_id) REFERENCES rides(ride_id) ON DELETE CASCADE,
        CONSTRAINT fk_rating_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        CONSTRAINT fk_rating_driver FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE
    );


    -- ==========================
    -- Indexes for Optimization
    -- ==========================
    CREATE INDEX idx_users_email ON users(email);
    CREATE INDEX idx_users_phone ON users(phone);
    CREATE INDEX idx_drivers_license ON drivers(license_number);
    CREATE INDEX idx_drivers_phone ON drivers(phone);
    CREATE INDEX idx_rides_user ON rides(user_id);
    CREATE INDEX idx_rides_driver ON rides(driver_id);
    CREATE INDEX idx_vehicles_driver ON vehicles(driver_id);
    
    
    
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    pass
