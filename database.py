"""
database.py
SQLAlchemy ORM models + session helpers
Supports SQLite (default) and PostgreSQL (set DATABASE_URL env var)
"""

import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    Text,
    JSON,
    Index,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Optional

# ── Connection ────────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./device_health.db",
)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ── Table 1: Raw Metrics ──────────────────────────────────────────────────────
class MetricRecord(Base):
    __tablename__ = "metric_records"

    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String(10), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Shared
    cpu_percent = Column(Float)
    ram_percent = Column(Float)
    battery_percent = Column(Float)
    battery_plugged = Column(Boolean)

    # Laptop only
    cpu_temp_c = Column(Float, nullable=True)
    cpu_freq_mhz = Column(Float, nullable=True)
    ram_used_gb = Column(Float, nullable=True)
    ram_total_gb = Column(Float, nullable=True)
    swap_percent = Column(Float, nullable=True)
    disk_used_pct = Column(Float, nullable=True)
    disk_read_mb = Column(Float, nullable=True)
    disk_write_mb = Column(Float, nullable=True)
    net_bytes_sent = Column(Float, nullable=True)
    net_bytes_recv = Column(Float, nullable=True)
    os_name = Column(String(30), nullable=True)
    hostname = Column(String(100), nullable=True)

    # Phone only
    battery_temp_c = Column(Float, nullable=True)
    battery_voltage_mv = Column(Integer, nullable=True)
    signal_dbm = Column(Float, nullable=True)
    signal_strength = Column(Float, nullable=True)
    storage_used_pct = Column(Float, nullable=True)
    uptime_hours = Column(Float, nullable=True)

    __table_args__ = (
        Index("idx_device_timestamp", "device_type", "timestamp"),
        Index("idx_cpu_percent", "cpu_percent"),
        Index("idx_ram_percent", "ram_percent"),
    )


# ── Table 2: Health Scores ────────────────────────────────────────────────────
class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String(10), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    health_score = Column(Integer)
    risk_level = Column(String(10))
    rul_days = Column(Integer)
    confidence_score = Column(Float)
    degradation_rate = Column(Float)
    component_scores = Column(JSON)
    failure_probs = Column(JSON)

    __table_args__ = (
        Index("idx_device_score_time", "device_type", "health_score", "timestamp"),
        Index("idx_risk_level", "risk_level"),
    )


# ── Table 3: Alerts ───────────────────────────────────────────────────────────
class AlertRecord(Base):
    __tablename__ = "alert_records"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(120), unique=True, index=True)
    device_type = Column(String(10), index=True)
    severity = Column(String(10))
    message = Column(Text)
    metric = Column(String(60))
    value = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    acknowledged = Column(Boolean, default=False)


# ── Table 4: Sessions ──────────────────────────────────────────────────────────
class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String(10))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    total_samples = Column(Integer, default=0)
    avg_health = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def row_to_dict(row):
    return {c.key: getattr(row, c.key) for c in row.__table__.columns}


def save_metric(db: Session, m: dict):
    row = MetricRecord(
        device_type=m.get("device_type"),
        timestamp=datetime.fromisoformat(m["timestamp"]),
        cpu_percent=m.get("cpu_percent"),
        ram_percent=m.get("ram_percent"),
        battery_percent=m.get("battery_percent"),
        battery_plugged=m.get("battery_plugged", False),
        cpu_temp_c=m.get("cpu_temp_c"),
        cpu_freq_mhz=m.get("cpu_freq_mhz"),
        ram_used_gb=m.get("ram_used_gb"),
        ram_total_gb=m.get("ram_total_gb"),
        swap_percent=m.get("swap_percent"),
        disk_used_pct=m.get("disk_used_pct"),
        disk_read_mb=m.get("disk_read_mb"),
        disk_write_mb=m.get("disk_write_mb"),
        net_bytes_sent=m.get("net_bytes_sent"),
        net_bytes_recv=m.get("net_bytes_recv"),
        os_name=m.get("os"),
        hostname=m.get("hostname"),
        battery_temp_c=m.get("battery_temp_c"),
        battery_voltage_mv=m.get("battery_voltage_mv"),
        signal_dbm=m.get("signal_dbm"),
        signal_strength=m.get("signal_strength"),
        storage_used_pct=m.get("storage_used_pct"),
        uptime_hours=m.get("uptime_hours"),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def save_health(db: Session, device_type: str, h: dict):
    row = HealthRecord(
        device_type=device_type,
        health_score=h["health_score"],
        risk_level=h["risk_level"],
        rul_days=h["rul_days"],
        confidence_score=h.get("confidence_score", 50),
        degradation_rate=h["degradation_rate"],
        component_scores=h["component_scores"],
        failure_probs=h["failure_probs"],
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def save_alerts(db: Session, device_type: str, alerts: list):
    for a in alerts:
        if (
            db.query(AlertRecord)
            .filter(AlertRecord.alert_id == a["id"])
            .first()
        ):
            continue
        db.add(
            AlertRecord(
                alert_id=a["id"],
                device_type=device_type,
                severity=a["severity"],
                message=a["message"],
                metric=a.get("metric", ""),
                value=a.get("value"),
                threshold=a.get("threshold"),
                timestamp=datetime.fromisoformat(a["timestamp"]),
            )
        )
    db.commit()
