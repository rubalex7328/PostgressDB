from connect import create_connection
import faker
from random import randint, choice

NUMBER_USERS = 5
NUMBER_TASKS = 10
NUMBER_STATUSES = 4


def generate_fake_data(number_users, number_tasks ) -> tuple():
    fake_users = []
    fake_emails = []
    fake_tasks = []
    fake_descriptions = []

    fake_data = faker.Faker()

    for _ in range(number_users):
        fake_users.append(fake_data.name())
        fake_emails.append(fake_data.email())

    fake_statuses = ["New","In Progress","Testing","Done"]

    for _ in range(number_tasks):
        fake_tasks.append(fake_data.sentence())
        fake_descriptions.append(fake_data.text(max_nb_chars=200))

    return fake_users, fake_emails, fake_statuses, fake_tasks,fake_descriptions


def prepare_data(users,emails,statuses,tasks,descriptions) -> tuple():
        #companies, employees, posts)

    for_statuses = []
    # готуємо список кортежів назв компаній
    for status in statuses:
        for_statuses.append((status, ))

    for_users = []
    for i in range(NUMBER_USERS):
        for_users.append((users[i],emails[i]))

    for_tasks = []
    for i in range(NUMBER_TASKS):
        for_tasks.append((tasks[i], descriptions[i], randint(1, NUMBER_STATUSES), randint(1, NUMBER_USERS) ))

    return for_users, for_statuses, for_tasks


def insert_data_to_db(users, statuses, tasks) -> None:
# Створимо з'єднання з нашою БД та отримаємо об'єкт курсора для маніпуляцій з даними

    with  create_connection() as con:
        with con.cursor() as cur:

            sql_to_users = """INSERT INTO users(fullname,email)
                                   VALUES (%s,%s)"""

            cur.executemany(sql_to_users, users)

            sql_to_statuses = """INSERT INTO status(name) VALUES (%s)"""

            cur.executemany(sql_to_statuses, statuses)

            sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id)
                                  VALUES (%s, %s, %s, %s)"""

            cur.executemany(sql_to_tasks, tasks)
            con.commit()


if __name__ == "__main__":
    users,statuses,tasks = prepare_data(*generate_fake_data(NUMBER_USERS,NUMBER_TASKS))
    insert_data_to_db(users,statuses,tasks)

