import logging
from psycopg2 import DatabaseError

from connect import create_connection



def create_db():
     # читаємо файл зі скриптом для створення БД
    with open('create_tables.sql', 'r') as f:
        sql = f.read()
    return sql

def create_table(conn, sql_expression: str):
    """ create a table from the create_table_sql statement
    :param sql_expression:
    :param conn: Connection object
    :return:
    """
    c = conn.cursor()
    try:
        c.execute(sql_expression)
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        c.close()


def create_connection():
    try:
        with create_connection() as conn:
            if conn is not None:
                ql_create_users_table = create_db()
                create_table(conn, sql_create_users_table)
            else:
                print("Error! cannot create the database connection.")
    except RuntimeError as err:
        logging.error(err)


if __name__ == '__main__':
    
    create_connection()