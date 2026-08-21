from sqlalchemy.orm import Session
import models
import schemas

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_student_id(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        student_id=student.student_id,
        name=student.name,
        gender=student.gender,
        major=student.major,
        email=student.email,
        phone=student.phone
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student: schemas.StudentUpdate):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        for var, value in vars(student).items():
            setattr(db_student, var, value) if value else None
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student
