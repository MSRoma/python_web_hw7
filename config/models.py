from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TeacherAlembic(Base):
    __tablename__ = 'teachers_alembic'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)

class GroupAlembic(Base):
    __tablename__ = 'groups_alembic'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class StudentAlembic(Base):
    __tablename__ = 'students_alembic'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column('group_id', ForeignKey('groups_alembic.id', ondelete='CASCADE'))
    group = relationship('GroupAlembic', backref='student')

class SubjectAlembic(Base):
    __tablename__ = 'subjects_alembic'
    id = Column(Integer, primary_key=True)
    name = Column(String(175), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers_alembic.id', ondelete='CASCADE'))
    teacher = relationship('TeacherAlembic', backref='subjects_alembic')

class GradeAlembic(Base):
    __tablename__ = 'grades_alembic'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    grade_date = Column('grade_date', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students_alembic.id', ondelete='CASCADE'))
    subjects_id = Column('subject_id', ForeignKey('subjects_alembic.id', ondelete='CASCADE'))
    student = relationship('StudentAlembic', backref='grade')
    discipline = relationship('SubjectAlembic', backref='grade')