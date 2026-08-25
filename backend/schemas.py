from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Student Schemas
class StudentBase(BaseModel):
    student_id: str = Field(..., description="学号")
    name: str = Field(..., description="姓名")
    gender: str = Field(..., description="性别")
    age: Optional[int] = Field(None, description="年龄")
    grade: str = Field(..., description="年级")
    major: str = Field(..., description="专业")
    contact: Optional[str] = Field(None, description="联系方式")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0, description="GPA")
    enrollment_date: date = Field(..., description="入学日期")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    major: Optional[str] = None
    contact: Optional[str] = None
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    enrollment_date: Optional[date] = None

class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaginatedStudentResponse(BaseModel):
    total: int
    items: list[Student]

# Course Schemas
class CourseBase(BaseModel):
    course_code: str
    name: str
    credits: int
    department: str
    teacher: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedCourseResponse(BaseModel):
    total: int
    items: list[Course]

# AuditLog Schemas
class AuditLogBase(BaseModel):
    username: str
    action: str
    entity_type: str
    entity_id: Optional[str]
    details: Optional[str]

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class PaginatedAuditLogResponse(BaseModel):
    total: int
    items: list[AuditLog]
