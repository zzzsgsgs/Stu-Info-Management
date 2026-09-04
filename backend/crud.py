from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
import models
import schemas
from fastapi import HTTPException

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_student_id(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 10, search: str = None, sort_by: str = None, sort_desc: bool = False):
    query = db.query(models.Student)

    if search:
        query = query.filter(
            or_(
                models.Student.name.ilike(f"%{search}%"),
                models.Student.major.ilike(f"%{search}%")
            )
        )

    if sort_by:
        column = getattr(models.Student, sort_by, None)
        if column:
            if sort_desc:
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = get_student_by_student_id(db, student.student_id)
    if db_student:
        raise HTTPException(status_code=400, detail="学号已存在")

    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student: schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return db_student

def log_audit(db: Session, username: str, action: str, entity_type: str, entity_id: str, details: str = None):
    audit_log = models.AuditLog(
        username=username,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        details=details
    )
    db.add(audit_log)
    db.commit()

def get_dashboard_stats(db: Session):
    total_students = db.query(models.Student).count()

    # Calculate gender ratio
    male_count = db.query(models.Student).filter(models.Student.gender == '男').count()
    female_count = db.query(models.Student).filter(models.Student.gender == '女').count()

    # Calculate average GPA
    from sqlalchemy.sql import func
    avg_gpa = db.query(func.avg(models.Student.gpa)).scalar() or 0.0

    # Calculate major distribution
    major_dist_query = db.query(models.Student.major, func.count(models.Student.id)).group_by(models.Student.major).all()
    major_dist = [{"name": row[0], "value": row[1]} for row in major_dist_query]

    return {
        "total_students": total_students,
        "gender_ratio": {"male": male_count, "female": female_count},
        "average_gpa": round(avg_gpa, 2),
        "major_distribution": major_dist
    }
