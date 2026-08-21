from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False) # 学号
    name = Column(String, index=True, nullable=False) # 姓名
    gender = Column(String, nullable=False) # 性别
    age = Column(Integer) # 年龄
    grade = Column(String) # 年级
    major = Column(String, index=True) # 专业
    contact = Column(String) # 联系方式
    gpa = Column(Float) # GPA
    enrollment_date = Column(Date) # 入学日期
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
