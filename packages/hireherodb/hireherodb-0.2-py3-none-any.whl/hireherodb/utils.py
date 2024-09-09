"""CRUD operations for managing companies, employees, job postings, candidates, and screenings in the database."""

from typing import List
from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_all_candidates_for_job(db: Session, job_id: int) -> List[schemas.Candidate]:
    """Get all candidates for a job from database."""
    rows = (
        db.query(models.Candidate)
        .filter(models.Candidate.job_posting_id == job_id)
        .all()
    )
    candidates = []
    for row in rows:
        candidate = schemas.Candidate.model_validate(row)
        candidates.append(candidate)
    return candidates


def get_all_jobs_of_company(db: Session, company_id: int) -> List[schemas.JobPosting]:
    """Get all jobs for a company from database."""
    rows = (
        db.query(models.JobPosting)
        .filter(models.JobPosting.company_id == company_id)
        .all()
    )
    jobpostings = []
    for row in rows:
        jobposting = schemas.JobPosting.model_validate(row)
        jobpostings.append(jobposting)
    return jobpostings


def get_all_employees_of_company(
    db: Session, company_id: int
) -> List[schemas.Employee]:
    """Get all employees for a company from database."""
    rows = (
        db.query(models.Employee).filter(models.Employee.company_id == company_id).all()
    )
    employees = []
    for row in rows:
        employee = schemas.Employee.model_validate(row)
        employees.append(employee)
    return employees


def create_screening(
    db: Session, screening: schemas.ScreeningCreate
) -> models.Screening:
    """Add screening to database."""
    db_screening = models.Screening(**screening.dict())
    db.add(db_screening)
    try:
        db.commit()
        db.refresh(db_screening)
    except Exception as e:
        db.rollback()
        print(f"Exception: {e}", flush=True)
        raise ValueError(f"Error creating screening: {e}")
    return db_screening


def get_all_screenings_for_job(db: Session, job_id: int) -> List[schemas.Screening]:
    """Get all screenings for a company from database."""
    rows = db.query(models.Screening).filter(models.Screening.job_id == job_id).all()
    screenings = []
    for row in rows:
        screening = schemas.Screening.model_validate(row)
        screenings.append(screening)
    return screenings


def get_all_screenings_for_candidate(
    db: Session, candidate_id: int
) -> List[schemas.Screening]:
    """Get all screenings for a candidate from database."""
    rows = (
        db.query(models.Screening)
        .filter(models.Screening.candidate_id == candidate_id)
        .all()
    )
    screenings = []
    for row in rows:
        screening = schemas.Screening.model_validate(row)
        screenings.append(screening)
    return screenings
