from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
import auth
import models
from database import get_db

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/", response_model=schemas.PaginatedCourseResponse)
def read_courses(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    query = db.query(models.Course)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}
