from connect import create_connection


def select_task_by_user(cursor,user_id):
    cursor.execute("""
        select t.* from tasks as t 
        where user_id = %s;"""
                   , (user_id,))
    return cursor.fetchall()


def select_task_by_status_name(cursor,status_name):
    cursor.execute("""
        select t.* 
        from tasks as t
        join status as s on t.status_id=s.id  
        where s.name = %s;"""
                   , (status_name,))
    return cursor.fetchall()


def update_task_status(cursor,task_id,status_name):
    sql = """
        update tasks
        set status_id = (select id from status where name=%s)
        where id=%s;
        """
    cursor.execute(sql,(status_name,task_id))


def select_users_without_task(cursor):
    cursor.execute("""
        select u.* 
        from users as u
        where u.id not in (select user_id from tasks);
    """)
    return cursor.fetchall()

def add_task_to_user(cursor,task):
    cursor.execute("""
        insert into tasks(title,description,status_id,user_id)
        values (%s, %s, (select id from status where name=%s),%s);
    """,task)


def select_task_not_in_status(cursor,status_name):
    cursor.execute("""
        select t.* 
        from tasks as t
        join status as s on t.status_id=s.id  
        where s.name <> %s;"""
                   , (status_name,))
    return cursor.fetchall()


def remove_task(cursor,task_id):
    cursor.execute("""
        delete from tasks where id = %s;""",(task_id,))


def select_user_by_email(cursor,email):
    cursor.execute("""
        select u.* 
        from users as u
        where u.email like %s;"""
                   , (email,))
    return cursor.fetchall()


def update_user_name(cursor,user_id,fullname):
    cursor.execute("""
        update users
        set fullname=%s
        where id = %s;""",(fullname,user_id))


def select_tasks_count(cursor):
    cursor.execute("""
        select count(t.*),s.name 
        from tasks as t
        join status as s on t.status_id=s.id        
        group by s.id;""")
    return cursor.fetchall()


def select_tasks_with_email(cursor,email):
    cursor.execute("""
        select t.* 
        from tasks as t
        join users as s on t.user_id=s.id        
        where s.email like %s;""",
                   (email,))
    return cursor.fetchall()


def select_tasks_without_description(cursor):
    cursor.execute("""
        select t.* 
        from tasks as t
        where t.description is null;""")
    return cursor.fetchall()


def select_task_and_users_with_status(cursor,status_name):
    cursor.execute("""
        select u.*,t.* 
        from tasks as t
        inner join users as u on u.id = t.user_id 
        inner join status as s on t.status_id=s.id  
        where s.name = %s;"""
                   , (status_name,))
    return cursor.fetchall()


def select_users_task_count(cursor):
    cursor.execute("""
        select u.*,count(t.*) 
        from users as u
        left join tasks as t on u.id = t.user_id 
        group by u.id;""")
    return cursor.fetchall()


def main():
    with  create_connection() as connection:
        with connection.cursor() as cursor:
            print("Tasks of user 2:")
            print(select_task_by_user(cursor,2))
            print("Tasks with status New:")
            print(select_task_by_status_name(cursor,"New"))
            print("Update status of task 2 to 'In Progress':")
            update_task_status(cursor,2, "In Progress")
            connection.commit()
            print("Users without tasks:")
            print(select_users_without_task(cursor))
            update_user_name(cursor,1,"Smith Sam")
            connection.commit()

            add_task_to_user(cursor,("Fix slack app","Fix bug #12378596","New",2))
            connection.commit()
            print("tasks not done:")
            print(select_task_not_in_status(cursor,"Done"))
            remove_task(cursor,1)
            connection.commit()
            print("Users in domain example.net")
            print(select_user_by_email(cursor,"%example.net"))
            print("Count of tasks by status")
            print(select_tasks_count(cursor))

            print("Tasks for users with domain 'example.com':")
            print(select_tasks_with_email(cursor,"%example.com"))
            print('select_tasks_without_description:')
            print(select_tasks_without_description(cursor))
            print("Users and tasks with status 'In Progress'")
            print(select_task_and_users_with_status(cursor,"in Progress"))
            print("Users with task count")
            print(select_users_task_count(cursor))


if __name__ == '__main__':
    main()