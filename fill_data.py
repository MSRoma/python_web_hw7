import datetime
import faker
import random
from random import randint, choice
from faker import Faker
import sqlite3

NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 20

def generate_fake_data(number_students, number_teachers, number_groups,number_subjects,number_grades) -> tuple():
    fake_students = []  # список студентів
    fake_teachers = []  # список викладачів
    fake_groups = []  # список груп
    fake_subjects = []  # список предметів
    fake_grades = []  # список оцінок
   
    fake_data = faker.Faker((['uk-UA']))

    # Створимо список студентів у кількості number_students
    for _ in range(number_students):
        fake_students.append(fake_data.name())

    # Згенеруємо тепер  список викладачів  у кількості number_students
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    # Згенеруємо  список груп у кількості number_groups
    for _ in range(number_groups):
        fake_groups.append(fake_data.safe_color_name())
    
    # Згенеруємо  список предметів у кількості umber_subjects
    for _ in range(number_subjects):
        fake_subjects.append(fake_data.job())
    
    fake_grades = number_grades
    # for _ in range(number_grades):
    #     fake_grades.append(fake_data.random_int(min=1,max = 12))

    return fake_students, fake_teachers, fake_groups, fake_subjects ,fake_grades


def prepare_data(students, teachers, groups ,subjects, grades) -> tuple():
    fake = Faker()
    for_groups = []
    # Готуємо список кортежів назв груп
    for group in groups:
        for_groups.append((group, ))
    
    for_students = []  # для таблиці студентів

    for std in students:
        '''
        Для записів у таблицю співробітників нам потрібно додати посаду та id компанії. Компаній у нас було за замовчуванням
        NUMBER_COMPANIES, при створенні таблиці companies для поля id ми вказували INTEGER AUTOINCREMENT - тому кожен
        запис отримуватиме послідовне число збільшене на 1, починаючи з 1. Тому компанію вибираємо випадково
        у цьому діапазоні
        '''
        for_students.append((std, fake.email(),randint(18, 59), randint(1, NUMBER_GROUPS)))

    '''
    Подібні операції виконаємо й у таблиці payments виплати зарплат. Приймемо, що виплата зарплати у всіх компаніях
    виконувалася з 10 по 20 числа кожного місяця. Діапазон зарплат генеруватимемо від 1000 до 10000 у.о.
    для кожного місяця, та кожного співробітника.
    '''
    for_teachers = []

    for teach in teachers:
        for_teachers.append((teach, ))

    for_subjects = []

    for sub in subjects:
        for_subjects.append((sub, randint(1, NUMBER_TEACHERS) ))
    
    for_grades = []

    for i in range(1, NUMBER_STUDENTS+1):
        for _ in range(grades):
            start_date = datetime.date(year=2015, month=1, day=1)
            end_date = datetime.date(year=2016, month=1, day=1)
            fake_dat = fake.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d")
            for_grades.append((randint(4, 12), i, randint(1, 8), fake_dat))

    return for_students, for_teachers, for_groups, for_subjects, for_grades

def insert_data_to_db(students, teachers, groups ,subjects, grades) -> None:
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсору для маніпуляцій з даними

    with sqlite3.connect('salary.db') as con:

        cur = con.cursor()

        '''Заповнюємо таблицю студентів. І створюємо скрипт для вставлення, де змінні, які вставлятимемо, відзначимо
        знаком заповнювача (?) '''

        sql_to_students = """INSERT INTO students(fullname, email, age, groups_id)
                               VALUES (?, ?, ?, ?)"""

        '''Для вставлення відразу всіх даних скористаємося методом executemany курсора. Першим параметром буде текст
        скрипта, а другим - дані (список кортежів).'''

        cur.executemany(sql_to_students, students)

        # Далі вставляємо дані про вчителів. Напишемо для нього скрипт і вкажемо змінні

        sql_to_teachers = """INSERT INTO teachers(fullname)
                               VALUES (?)"""

        # Дані були підготовлені заздалегідь, тому просто передаємо їх у функцію

        cur.executemany(sql_to_teachers, teachers)

        # Заповнюємо таблицю із вчителями

        sql_to_groups = """INSERT INTO groups(groups_name)
                              VALUES (?)"""

        # Вставляємо дані про групи

        cur.executemany(sql_to_groups, groups)

        sql_to_subjects = """INSERT INTO subjects(subjects_name, teachers_id)
                              VALUES (?, ?)"""

        # Вставляємо дані про предмети

        cur.executemany(sql_to_subjects, subjects)

        sql_to_grades = """INSERT INTO grades(grades, student_id, subject_id, created_at)
                              VALUES (?, ?, ?, ?)"""

        # Вставляємо дані про оцінки

        cur.executemany(sql_to_grades, grades)

        # Фіксуємо наші зміни в БД

        con.commit()



if __name__ == "__main__":
    #students, teachers, groups ,subjects, grades = generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_GROUPS,NUMBER_SUBJECTS,NUMBER_GRADES)

    students_db, teachers_db, groups_db ,subjects_db, grades_db = prepare_data(*generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_GROUPS,NUMBER_SUBJECTS,NUMBER_GRADES))

    insert_data_to_db(students_db, teachers_db, groups_db ,subjects_db, grades_db)   
  