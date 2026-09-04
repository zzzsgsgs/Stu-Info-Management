from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth_router, students_router, courses_router, system_router

app = FastAPI(title="Student Info Management System API v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(students_router.router)
app.include_router(courses_router.router)
app.include_router(system_router.router)
