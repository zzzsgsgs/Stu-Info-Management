from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Optional
import csv
import io
import schemas
import crud
import auth
from database import get_db

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    new_student = crud.create_student(db=db, student=student)
    crud.log_audit(db, current_user.username, "CREATE", "Student", new_student.student_id, f"Created student {new_student.name}")
    return new_student

@router.get("/", response_model=schemas.PaginatedStudentResponse)
def read_students(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_desc: bool = False,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.get_students(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)

from fastapi import Query

@router.get("/export")
def export_students_csv(
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    # Manually verify token from query parameter for file download
    try:
        from jose import jwt
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    students = crud.get_students(db, skip=0, limit=10000)["items"]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "学号", "姓名", "性别", "年龄", "年级", "专业", "GPA", "联系方式", "入学日期"])

    for s in students:
        writer.writerow([s.id, s.student_id, s.name, s.gender, s.age, s.grade, s.major, s.gpa, s.contact, s.enrollment_date])

    response = Response(content=output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=students_export.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"

    crud.log_audit(db, username, "EXPORT", "Student", "ALL", "Exported student list")
    return response

@router.get("/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.put("/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    updated_student = crud.update_student(db=db, student_id=student_id, student=student)
    crud.log_audit(db, current_user.username, "UPDATE", "Student", updated_student.student_id, f"Updated student {updated_student.name}")
    return updated_student

@router.delete("/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    deleted_student = crud.delete_student(db=db, student_id=student_id)
    crud.log_audit(db, current_user.username, "DELETE", "Student", deleted_student.student_id, f"Deleted student {deleted_student.name}")
    return deleted_student
