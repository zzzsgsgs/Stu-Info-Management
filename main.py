from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Info Management API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    if not db.query(models.Student).first():
        dummy_students = [
            schemas.StudentCreate(student_id="S001", name="Alice Smith", gender="Female", major="Computer Science", email="alice@example.com", phone="123-456-7890"),
            schemas.StudentCreate(student_id="S002", name="Bob Johnson", gender="Male", major="Mathematics", email="bob@example.com", phone="234-567-8901"),
            schemas.StudentCreate(student_id="S003", name="Charlie Brown", gender="Male", major="Physics", email="charlie@example.com", phone="345-678-9012"),
            schemas.StudentCreate(student_id="S004", name="Diana Prince", gender="Female", major="History", email="diana@example.com", phone="456-789-0123"),
            schemas.StudentCreate(student_id="S005", name="Eve Davis", gender="Female", major="Biology", email="eve@example.com", phone="567-890-1234"),
        ]
        for student in dummy_students:
            crud.create_student(db=db, student=student)
    db.close()

@app.post("/api/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_student_id(db, student_id=student.student_id)
    if db_student:
        raise HTTPException(status_code=400, detail="Student ID already registered")
    return crud.create_student(db=db, student=student)

@app.get("/api/students/", response_model=List[schemas.StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.get("/api/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.put("/api/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.update_student(db=db, student_id=student_id, student=student)

@app.delete("/api/students/{student_id}", response_model=schemas.StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.delete_student(db=db, student_id=student_id)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
