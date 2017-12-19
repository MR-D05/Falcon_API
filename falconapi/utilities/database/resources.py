import psycopg2
from falconapi.config import DATABASE_URL

def connection():
    connection = psycopg2.connect(DATABASE_URL)
    connection.set_session(autocommit=True)
    return connection

def get_user(cursor, username):
    cursor.execute(
        "SELECT (id), (encrypted_password) FROM users WHERE (username) = (%s)", (username,))
    result = cursor.fetchone()
    return result


def get_token(cursor, user_id):
    cursor.execute(
        "SELECT (token) FROM api_tokens WHERE (user_id) = (%s)", (user_id,))
    result = cursor.fetchone()
    return result


def insert_token(cursor, token, user_id):
    cursor.execute(
        "INSERT INTO api_tokens (token, user_id) VALUES (%s, %s)", (token, user_id,))
    print('New session token has been generated.')
    cursor.execute(
        "SELECT (token) FROM api_tokens WHERE (user_id) = (%s)", (user_id,))
    result = cursor.fetchone()
    return result


def has_token(cursor, user_id):
    cursor.execute(
        "SELECT (token), (user_id) FROM api_tokens WHERE (user_id) = (%s)", (user_id,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def is_admin(cursor, username):
    cursor.execute(
        "SELECT (is_admin) FROM users WHERE (username) = (%s)", (username,))
    result = cursor.fetchone()[0]
    print(result)
    if result == True:
        return True
    else:
        return False


def get_id(cursor, token):
    cursor.execute(
        "SELECT (user_id) FROM api_tokens WHERE (token) = (%s)", (token,))
    result = cursor.fetchone()
    return result


def get_name(cursor, user_id):
    cursor.execute(
        "SELECT (username) FROM users WHERE (id) = (%s)", (user_id,))
    result = cursor.fetchone()
    return result


def insert_file(cursor, filename, username, uuid):
    cursor.execute(
        "INSERT INTO files (filename, username, uuid) VALUES (%s, %s, %s)", (filename, username, uuid,))
    print('New file inserted into database.')


def get_files(cursor, username):
    cursor.execute(
        "SELECT * FROM files WHERE (username) = (%s)", (username,))
    result = cursor.fetchall()
    return result

