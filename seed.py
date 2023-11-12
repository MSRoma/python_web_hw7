from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, String, Integer, Text, ForeignKey,Date
from config.db import session , engine
from  config.models import TeacherAlembic, GroupAlembic, StudentAlembic, SubjectAlembic ,GradeAlembic
from faker import Faker
from random import randint


NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 20

Base = declarative_base()

fake = Faker((['uk-UA']))

Base.metadata.create_all(engine)
Base.metadata.bind = engine

for _ in range(NUMBER_TEACHERS):
    new_teachers = TeacherAlembic(fullname=fake.name())
    session.add(new_teachers)

for _ in range(NUMBER_GROUPS):
    new_groups = GroupAlembic(name=fake.safe_color_name())
    session.add(new_groups)

for _ in range(NUMBER_STUDENTS):
    new_student = StudentAlembic(fullname=fake.name(), group_id=randint(1, NUMBER_GROUPS ) )
    session.add(new_student)

for _ in range(NUMBER_SUBJECTS):
    new_subjects = SubjectAlembic(name=fake.job(), teacher_id=randint(1, NUMBER_TEACHERS) )
    session.add(new_subjects)

for num_st in range(1, NUMBER_STUDENTS + 1):
    for _ in range(NUMBER_GRADES):
        new_grade = GradeAlembic(grade=randint(4, 12), grade_date=fake.date_this_decade(),student_id=num_st, subjects_id=randint(1, NUMBER_SUBJECTS))
        session.add(new_grade)


session.commit()
