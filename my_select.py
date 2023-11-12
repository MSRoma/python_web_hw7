from sqlalchemy import func, desc, select, and_

from  config.models import TeacherAlembic, GroupAlembic, StudentAlembic, SubjectAlembic ,GradeAlembic
from config.db import session


def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students_alembic s
    JOIN grades_alembic g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(StudentAlembic.id, StudentAlembic.fullname, func.round(func.avg(GradeAlembic.grade), 2).label('average_grade')) \
        .select_from(StudentAlembic).join(GradeAlembic).group_by(StudentAlembic.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade,
    FROM grades_alembic g
    JOIN students_alembic s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(StudentAlembic.id, StudentAlembic.fullname, func.round(func.avg(GradeAlembic.grade), 2).label('average_grade')) \
        .select_from(GradeAlembic).join(StudentAlembic).filter(GradeAlembic.subjects_id == 1).group_by(StudentAlembic.id).order_by(
        desc('average_grade')).limit(1).all()
    return result

def select_03():
    """
    SELECT
        g.name,
        ROUND(AVG(gr.grade)) as avg_grade
    FROM grades_alembic as gr
    JOIN students_alembic as st on st.id = gr.student_id
    JOIN groups_alembic as g on g.id = st.group_id
    WHERE gr.subject_id = 3
    GROUP BY g.name;
    """
    result = session.query(GroupAlembic.name, func.round(func.avg(GradeAlembic.grade)).label('avg_grade')) \
        .select_from(GradeAlembic).join(StudentAlembic).join(GroupAlembic).filter(GradeAlembic.subjects_id == 3).group_by(GroupAlembic.name).all()
    return result


def select_04():
    """
    SELECT
        ROUND(AVG(gr.grade)) as avg_grade
    FROM grades_alembic as g
    """
    result = session.query(func.round(func.avg(GradeAlembic.grade)).label('avg_grade')) \
        .select_from(GradeAlembic).all()
    return result


def select_05():
    """
    SELECT
        t.fullname,sb.name
    FROM teachers_alembic as t
    JOIN subjects_alembic as sb on t.id = sb.teacher_id
    WHERE t.id = 5;
 
    """
    result = session.query(TeacherAlembic.fullname, SubjectAlembic.name ) \
        .select_from(TeacherAlembic).join(SubjectAlembic).filter(TeacherAlembic.id == 5).all()
    return result

def select_06():
    """
    SELECT
        g.name, s.fullname
    FROM groups_alembic as g
    JOIN students_alembic as s on g.id = s.group_id
    WHERE g.id = 2;
 
    """
    result = session.query(GroupAlembic.name, StudentAlembic.fullname ) \
        .select_from(GroupAlembic).join(StudentAlembic).filter(GroupAlembic.id == 2).all()
    return result

def select_07():
    """
    SELECT
        s.fullname, g.name, gr.grade,sb.name  
    FROM students_alembic as s
    JOIN grades_alembic as gr on gr.student_id = s.id
    JOIN groups_alembic as g on g.id = s.group_id
    JOIN subjects_alembic as sb on s.group_id = sb.id
    WHERE gr.subject_id = 2
    AND g.id = 2
 
    """
    result = session.query(StudentAlembic.fullname, GroupAlembic.name,GradeAlembic.grade,SubjectAlembic.name ) \
        .select_from(StudentAlembic).join(GradeAlembic).join(GroupAlembic).join(SubjectAlembic).filter(GradeAlembic.subjects_id == 2,GroupAlembic.id == 2).all()
    return result


def select_08():
    """
    SELECT 
        t.fullname,
        sb.name,
        ROUND(AVG(gr.grade), 2) AS average_grade
    FROM teachers_alembic as t
    JOIN subjects_alembic sb ON sb.teacher_id = t.id
    JOIN grades_alembic gr ON gr.subject_id = sb.id
    where t.id = 4
    group by  sb.name ,t.fullname  
    ORDER BY average_grade DESC
 
    """
    result = session.query(TeacherAlembic.fullname, SubjectAlembic.name, func.round(func.avg(GradeAlembic.grade), 2).label('average_grade')) \
        .select_from(TeacherAlembic).join(SubjectAlembic).join(GradeAlembic).filter(TeacherAlembic.id == 4).group_by(SubjectAlembic.name,TeacherAlembic.fullname).order_by(
        desc('average_grade')).all()
    return result



def select_09():
    """
    SELECT
        st.fullname, sb.name
    FROM subjects_alembic as sb
    JOIN grades_alembic as gr on gr.subject_id = sb.id
    JOIN students_alembic as st on st.id = gr.student_id
    where st.id = 5
    group by sb.name, st.fullname
 
    """
    result = session.query(StudentAlembic.fullname, SubjectAlembic.name) \
        .select_from(SubjectAlembic).join(GradeAlembic).join(StudentAlembic).filter(StudentAlembic.id == 2).group_by(SubjectAlembic.name,StudentAlembic.fullname).all()
    return result


def select_10():
    """
    SELECT
        st.fullname, sb.name ,t.fullname
    FROM subjects_alembic as sb
    JOIN grades_alembic as gr on gr.subject_id = sb.id
    JOIN students_alembic as st on st.id = gr.student_id
    JOIN teachers_alembic as t on t.id = sb.teacher_id
    where st.id = 5
    and t.id = 5
    group by sb.name, st.fullname ,t.fullname
 
    """
    result = session.query(StudentAlembic.fullname, SubjectAlembic.name, TeacherAlembic.fullname ) \
        .select_from(SubjectAlembic).join(GradeAlembic).join(StudentAlembic).join(TeacherAlembic).filter(StudentAlembic.id == 2, TeacherAlembic.id == 4) \
            .group_by(SubjectAlembic.name,StudentAlembic.fullname,TeacherAlembic.fullname ).all()
    return result


if __name__ == '__main__':
    print(select_01())
    #print(select_02())
    #print(select_03())
    #print(select_04())
    #print(select_05())
    #print(select_06())
    #print(select_07())
    #print(select_08())
    #print(select_09())
    # print(select_10())
