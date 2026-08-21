from pydantic import BaseModel

class StudentBase(BaseModel):
    student_id: str
    name: str
    gender: str
    major: str
    email: str
    phone: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
