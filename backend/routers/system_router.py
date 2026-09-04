from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
import schemas
import crud
import auth
import models
from database import get_db

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/dashboard")
def read_dashboard_stats(db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.get_dashboard_stats(db)

@router.get("/audit-logs", response_model=schemas.PaginatedAuditLogResponse)
def read_audit_logs(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    query = db.query(models.AuditLog).order_by(desc(models.AuditLog.timestamp))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}
