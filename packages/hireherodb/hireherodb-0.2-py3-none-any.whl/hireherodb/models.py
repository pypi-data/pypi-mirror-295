"""This module contains the SQLAlchemy models for the database tables."""

from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Company(Base):  # type: ignore
    """This class represents the companies table in the database."""

    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    industry = Column(String(255))
    description = Column(Text)
    website = Column(String(255))
    headquarters = Column(String(255))
    size = Column(String(50))
    logo_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    employees = relationship(
        "Employee", back_populates="company", cascade="all, delete"
    )
    job_postings = relationship(
        "JobPosting", back_populates="company", cascade="all, delete"
    )


class Employee(Base):  # type: ignore
    """This class represents the employees table in the database."""

    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    job_title = Column(String(255))
    phone = Column(String(20))
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    company = relationship("Company", back_populates="employees")


class JobPosting(Base):  # type: ignore
    """This class represents the job_postings table in the database."""

    __tablename__ = "job_posting"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    location = Column(String)
    employment_type = Column(String)
    description = Column(Text)
    key_responsibilities = Column(Text)
    required_qualifications = Column(Text)
    preferred_qualifications = Column(Text)
    other_info = Column(ARRAY(String))
    posted_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    salary = Column(Float, nullable=True, default=0.0)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    company = relationship("Company", back_populates="job_postings")
    candidates = relationship(
        "Candidate", back_populates="job_posting", cascade="all, delete"
    )
    screenings = relationship(
        "Screening", back_populates="job_posting", cascade="all, delete"
    )


class Candidate(Base):  # type: ignore
    """This class represents the candidate_profiles table in the database."""

    __tablename__ = "candidate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    summary = Column(String)
    education = Column(JSON)
    experience = Column(JSON)
    skills = Column(JSON)
    projects = Column(JSON)
    certifications = Column(JSON)
    publications = Column(JSON)
    references = Column(JSON)
    links = Column(JSON)
    additional_info = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    job_posting_id = Column(Integer, ForeignKey("job_posting.id"), nullable=False)
    job_posting = relationship("JobPosting", back_populates="candidates")
    screening = relationship(
        "Screening", back_populates="candidate", cascade="all, delete"
    )


class Screening(Base):  # type: ignore
    """This class represents the screenings table in the database."""

    __tablename__ = "screening"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("job_posting.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidate.id"), nullable=False)
    questions_and_answers = Column(JSON, nullable=False)
    final_score = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    job_posting = relationship("JobPosting", back_populates="screenings")
    candidate = relationship("Candidate", back_populates="screening")


# Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
