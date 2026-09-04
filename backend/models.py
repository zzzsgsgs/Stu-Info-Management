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

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False) # 课程代码
    name = Column(String, index=True, nullable=False) # 课程名称
    credits = Column(Integer, nullable=False) # 学分
    department = Column(String) # 开课学院
    teacher = Column(String) # 授课教师
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True, nullable=False) # 关联学生ID
    course_id = Column(Integer, index=True, nullable=False) # 关联课程ID
    semester = Column(String, nullable=False) # 学期 (如 2023-秋)
    score = Column(Float) # 最终成绩
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True) # 操作人
    action = Column(String, nullable=False) # 动作 (CREATE/UPDATE/DELETE)
    entity_type = Column(String, nullable=False) # 实体类型 (Student/Course)
    entity_id = Column(String) # 被操作的实体ID
    details = Column(String) # 详细信息 (JSON string)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
