from flask import session
from confidb import get_conexion


def iniciar_log(email, password):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()
    cnn.close()
    return account

def register_log(name):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE name = %s', (name))
        account1 = cursor.fetchone()
    cnn.close()
    return account1

def busc_datos(name, email, password, photo):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s)', (name, email, password, photo))
    cnn.commit()
    cnn.close()   

"""
def profile():
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE id = %s', (id))
        account2 = cursor.fetchone()
    cnn.close()
    return account2
    """
def profile():
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
    cnn.close()
    return account