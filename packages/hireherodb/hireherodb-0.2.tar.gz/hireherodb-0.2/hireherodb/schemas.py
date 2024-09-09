"""Pydantic schemas for Company, Employee, JobPosting, Candidate, and Screening models with ORM support."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr


class CompanyBase(BaseModel):
    """Pydantic base schema for company."""

    name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    size: Optional[str] = None
    logo_url: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Pydantic create schema for company."""

    pass


class Company(CompanyBase):
    """Pydantic output schema for company."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """activate orm pydantic relationship."""

        from_attributes = True


class EmployeeBase(BaseModel):
    """Pydantic base schema for employee."""

    name: str
    email: EmailStr
    job_title: Optional[str] = None
    phone: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    """Pydantic create schema for employee."""

    company_id: int


class Employee(EmployeeBase):
    """Pydantic output schema for employee."""

    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """activate orm pydantic relationship."""

        from_attributes = True


class JobPostingBase(BaseModel):
    """Pydantic base schema for jobposting."""

    title: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None
    key_responsibilities: Optional[str] = None
    required_qualifications: Optional[str] = None
    preferred_qualifications: Optional[str] = None
    other_info: Optional[List[str]] = None
    salary: Optional[float] = None


class JobPostingCreate(JobPostingBase):
    """Pydantic create schema for jobposting."""

    company_id: int


class JobPosting(JobPostingBase):
    """Pydantic output schema for jobposting."""

    id: int
    company_id: int
    posted_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        """activate orm pydantic relationship."""

        from_attributes = True


class CandidateBase(BaseModel):
    """Pydantic base schema for candidate."""

    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    summary: Optional[str] = None
    education: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    publications: Optional[List[Dict[str, Any]]] = None
    references: Optional[List[Dict[str, Any]]] = None
    links: Optional[Dict[str, str]] = None
    additional_info: Optional[Dict[str, Any]] = None


class CandidateCreate(CandidateBase):
    """Pydantic create schema for candidate."""

    job_posting_id: int


class Candidate(CandidateBase):
    """Pydantic output schema for candidate."""

    id: int
    job_posting_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """activate orm pydantic relationship."""

        from_attributes = True


class ScreeningBase(BaseModel):
    """Pydantic base schema for screening."""

    job_id: int
    candidate_id: int
    questions_and_answers: List[Dict[str, str]]
    final_score: int


class ScreeningCreate(ScreeningBase):
    """Pydantic create schema for screening."""

    pass


class Screening(ScreeningBase):
    """Pydantic output schema for screening."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """activate orm pydantic relationship."""

        from_attributes = True
