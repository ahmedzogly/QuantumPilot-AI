"""
SQLAlchemy Models - Persistence Layer for QuantumPilot AI
Domain: User, Project, Circuit, ExecutionDecision, ExecutionResult, BackendCalibration cache
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base

def gen_uuid():
    return str(uuid.uuid4())

class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProjectModel(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("UserModel")

class CircuitModel(Base):
    __tablename__ = "circuits"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String)
    qasm = Column(Text)
    qiskit_code = Column(Text)
    profile_json = Column(JSON)  # CircuitProfile as JSON (includes Q-LEAR features)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("ProjectModel")

class BackendCalibrationModel(Base):
    __tablename__ = "backend_calibrations"
    id = Column(String, primary_key=True, default=gen_uuid)
    backend_name = Column(String, index=True)  # ibm_fez, marrakesh, kingston
    num_qubits = Column(Integer)
    last_update = Column(DateTime)
    T1_mean = Column(Float)
    T2_mean = Column(Float)
    readout_error_mean = Column(Float)
    cz_error_mean = Column(Float)
    cz_error_std = Column(Float)
    queue_length = Column(Integer, default=0)
    pending_jobs = Column(Integer, default=0)
    calibration_age_seconds = Column(Float, default=0)
    full_properties_json = Column(JSON)  # full live properties from ibm_live_properties.json
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionModel(Base):
    __tablename__ = "execution_decisions"
    id = Column(String, primary_key=True, default=gen_uuid)
    circuit_id = Column(String, ForeignKey("circuits.id"))
    backend_name = Column(String)
    optimization_level = Column(Integer)  # 0-3
    mitigation_strategy = Column(String)  # s_zne, zne, pec, trex, nnas, transformer, daem
    resilience_level = Column(Integer, default=1)
    shots = Column(Integer, default=4096)
    expected_fidelity = Column(Float)
    expected_cost = Column(Float)
    expected_queue = Column(Float)
    confidence = Column(Float)
    context_vector = Column(JSON)  # 22-D
    created_at = Column(DateTime, default=datetime.utcnow)
    circuit = relationship("CircuitModel")

class ResultModel(Base):
    __tablename__ = "execution_results"
    id = Column(String, primary_key=True, default=gen_uuid)
    decision_id = Column(String, ForeignKey("execution_decisions.id"))
    backend_name = Column(String)
    success = Column(Boolean, default=False)
    fidelity = Column(Float, nullable=True)
    hellinger_fidelity = Column(Float, nullable=True)
    execution_time_ms = Column(Integer, default=0)
    queue_time_ms = Column(Integer, default=0)
    cost_seconds = Column(Float, default=0)
    counts = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    mitigation_applied = Column(Boolean, default=False)
    reward = Column(Float, default=0.0)  # computed multi-objective
    created_at = Column(DateTime, default=datetime.utcnow)
    decision = relationship("DecisionModel")
