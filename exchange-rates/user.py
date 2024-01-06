import time
import psycopg2
from psycopg2 import OperationalError

# Параметры подключения к базе данных
db_params = {
    'dbname': 'curs_md_bot',
    'user': 'postgres',
    'password': '27102010Postgresql',
    'host': 'localhost',  # localhost, так как база данных находится в Docker на том же хосте
    'port': 6001          # Порт, который вы открыли в docker-compose
}


def connect():
    """ Подключение к базе данных с несколькими попытками """
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            conn = psycopg2.connect(**db_params)
            print("Подключение к базе данных успешно")
            return conn
        except OperationalError as e:
            attempts += 1
            print(f"Не удалось подключиться к базе данных, попытка номер {attempts}. Ошибка: {e}")
            time.sleep(5)  # Задержка 5 секунд
            if attempts == max_attempts:
                raise Exception("Не удалось подключиться к базе данных после нескольких попыток")

def add_user(user_id, username):
    """ Добавление пользователя, если он не существует """
    print(f"Добавление пользователя: user_id={user_id}, username={username}")

    conn = connect()
    cur = conn.cursor()

    # Проверяем, существует ли пользователь
    cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s);", (user_id,))
    exists = cur.fetchone()[0]

    if not exists:
        # Добавляем пользователя
        cur.execute("INSERT INTO users (user_id, username) VALUES (%s, %s);",
                    (user_id, username))
        conn.commit()
        print("Пользователь успешно добавлен в базу данных.")
    else:
        print("Пользователь с таким ID уже существует в базе данных. Не добавляем.")

    cur.close()
    conn.close()

def update_user_info(user_id, username):
    """ Обновление информации о пользователе """
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username = %s WHERE user_id = %s;",
                (username, user_id))
    conn.commit()
    cur.close()
    conn.close()



def add_bank(bank_name):
    """ Добавление банка """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO banks (bank_name) VALUES (%s);", (bank_name,))
    conn.commit()
    cur.close()
    conn.close()

def add_subscription(user_id, bank_id):
    """ Добавление подписки """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO subscriptions (user_id, bank_id) VALUES (%s, %s);",
                (user_id, bank_id))
    conn.commit()
    cur.close()
    conn.close()

def get_users():
    """ Получение списка пользователей """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

# # Примеры использования
# add_user(1, 'username1', '+37368268443')
# add_bank('Bank1')
# add_subscription(1, 1)
# users = get_users()
# print(users)
