import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
from models import User
from auth import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Create test admin
    hashed_password = get_password_hash("testpassword")
    test_user = User(username="testadmin", hashed_password=hashed_password)
    db.add(test_user)
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)

def test_login():
    response = client.post(
        "/token",
        data={"username": "testadmin", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail():
    response = client.post(
        "/token",
        data={"username": "testadmin", "password": "wrongpassword"},
    )
    assert response.status_code == 401

def test_export_students():
    login_res = client.post(
        "/token",
        data={"username": "testadmin", "password": "testpassword"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/students/export?token={token}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "ID,学号,姓名,性别" in response.text

def test_system_audit_logs():
    login_res = client.post(
        "/token",
        data={"username": "testadmin", "password": "testpassword"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/system/audit-logs", headers=headers)
    assert response.status_code == 200
    assert "total" in response.json()

def test_create_read_student():
    # Login first
    login_res = client.post(
        "/token",
        data={"username": "testadmin", "password": "testpassword"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create student
    student_data = {
        "student_id": "T001",
        "name": "Test Student",
        "gender": "男",
        "age": 20,
        "grade": "大二",
        "major": "测试专业",
        "contact": "123456",
        "gpa": 3.8,
        "enrollment_date": "2022-09-01"
    }
    response = client.post("/students/", json=student_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Student"

    # Read students
    response = client.get("/students/", headers=headers)
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["student_id"] == "T001"
