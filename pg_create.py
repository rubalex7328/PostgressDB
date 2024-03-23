import psycopg2
from connect import create_connection

create_table_tasks_query = """
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  status_id INT,
  user_id INT,
  FOREIGN KEY (status_id) REFERENCES status (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

create_table_users_query = """
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(30),
  email VARCHAR(30),
  CONSTRAINT users_email_un UNIQUE  (email)
);
"""

create_table_status_query = """
CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  CONSTRAINT status_name_un UNIQUE  (name)
);
"""

if __name__ == '__main__':
    with  create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_table_status_query)
            cursor.execute(create_table_users_query)
            cursor.execute(create_table_tasks_query)
