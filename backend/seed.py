import random
from datetime import date, timedelta
from database import SessionLocal
from models import User, Student, Course, Enrollment, AuditLog
from auth import get_password_hash

# 示例姓名
first_names = ["伟", "芳", "娜", "敏", "静", "强", "磊", "洋", "艳", "杰", "娟", "勇", "涛", "明", "霞", "秀英", "超", "军", "平", "刚"]
last_names = ["王", "李", "张", "刘", "陈", "杨", "黄", "赵", "吴", "周", "徐", "孙", "马", "朱", "胡", "郭", "林", "何", "高", "梁"]
majors = ["计算机科学与技术", "软件工程", "信息安全", "数据科学", "人工智能", "工商管理", "会计学", "金融学", "土木工程", "电子工程"]
grades = ["大一", "大二", "大三", "大四"]

def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def seed_db():
    db = SessionLocal()

    # 1. 检查并创建 Admin 用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        hashed_password = get_password_hash("admin")
        admin_user = User(username="admin", hashed_password=hashed_password)
        db.add(admin_user)
        print("Created default admin user (admin/admin)")

    # 2. 检查并生成模拟学生数据
    if db.query(Student).count() == 0:
        students_to_add = []
        for i in range(1, 31):
            name = f"{random.choice(last_names)}{random.choice(first_names)}"
            gender = random.choice(["男", "女"])
            student_id = f"2023{str(i).zfill(4)}"
            age = random.randint(18, 22)
            grade = random.choice(grades)
            major = random.choice(majors)
            contact = f"138{random.randint(10000000, 99999999)}"
            gpa = round(random.uniform(2.0, 4.0), 2)
            enrollment_date = generate_random_date(date(2020, 9, 1), date(2023, 9, 1))

            student = Student(
                student_id=student_id,
                name=name,
                gender=gender,
                age=age,
                grade=grade,
                major=major,
                contact=contact,
                gpa=gpa,
                enrollment_date=enrollment_date
            )
            students_to_add.append(student)

        db.add_all(students_to_add)
        db.commit() # Commit to get IDs
        print(f"Created 30 mock student records.")

    # 3. 检查并生成模拟课程数据
    if db.query(Course).count() == 0:
        courses_to_add = [
            Course(course_code="CS101", name="计算机编程基础", credits=4, department="计算机科学与技术", teacher="王老师"),
            Course(course_code="MA102", name="高等数学", credits=5, department="数学系", teacher="李老师"),
            Course(course_code="EN103", name="大学英语", credits=3, department="外语系", teacher="张老师"),
            Course(course_code="PH104", name="大学物理", credits=4, department="物理系", teacher="刘老师"),
            Course(course_code="EC105", name="微观经济学", credits=3, department="经济管理学院", teacher="陈老师"),
        ]
        db.add_all(courses_to_add)
        db.commit()
        print(f"Created mock course records.")

    # 4. 生成模拟选课数据和操作日志
    if db.query(Enrollment).count() == 0:
        students = db.query(Student).all()
        courses = db.query(Course).all()

        enrollments_to_add = []
        logs_to_add = []

        for student in students:
            # 随机选 2-4 门课
            selected_courses = random.sample(courses, random.randint(2, 4))
            for course in selected_courses:
                enrollments_to_add.append(
                    Enrollment(
                        student_id=student.id,
                        course_id=course.id,
                        semester="2023-秋",
                        score=round(random.uniform(60.0, 100.0), 1)
                    )
                )
            # 添加一些随机的操作日志
            logs_to_add.append(
                AuditLog(
                    username="admin",
                    action="CREATE",
                    entity_type="Student",
                    entity_id=student.student_id,
                    details=f"Created student via seed"
                )
            )

        db.add_all(enrollments_to_add)
        db.add_all(logs_to_add)
        db.commit()
        print(f"Created mock enrollment and audit log records.")

    db.close()
    print("Database seeding completed.")

if __name__ == "__main__":
    seed_db()
