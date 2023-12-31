"""init

Revision ID: 51999e325b86
Revises: 
Create Date: 2023-11-11 19:29:24.446923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51999e325b86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.drop_table('subjects')
    op.drop_table('grades')
    op.drop_table('teachers')
    op.drop_table('groups')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('groups_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='groups_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('teachers',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('teachers_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('fullname', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='teachers_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('grades',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('subject_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('grade', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('grade_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.CheckConstraint('grade >= 0 AND grade <= 100', name='grades_grade_check'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name='grades_student_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], name='grades_subject_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='grades_pkey')
    )
    op.create_table('subjects',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=175), autoincrement=False, nullable=False),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='subjects_teacher_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='subjects_pkey')
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fullname', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='students_group_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='students_pkey')
    )
    # ### end Alembic commands ###
