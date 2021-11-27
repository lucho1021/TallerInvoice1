from flask.config import ConfigAttribute
from confidb import get_conexion

def add_factura(date, price, balance, id):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute("INSERT INTO invoicet (date, price, balance, id) VALUES (%s, %s, %s, %s)", (date, price, balance, id))
    cnn.commit()
    cnn.close()

def update_factura(date, price, balance, number):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute("UPDATE invoicet SET date = %s, price = %s, balance = %s WHERE number = %s", (date, price, balance, number))
    cnn.commit()
    cnn.close()

def delete_factura(number):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute("DELETE FROM invoicet WHERE number = %s", (number))
    cnn.commit()
    cnn.close()

def get_facturas():
    cnn = get_conexion()
    facturas = []
    with cnn.cursor() as cursor:
        cursor.execute("SELECT number, date, id, price, balance FROM invoicet")
        facturas = cursor.fetchall()
    cnn.close()
    return facturas

def get_facturas_number(number):
    cnn = get_conexion()
    factura = None
    with cnn.cursor() as cursor:
        cursor.execute("SELECT number, date, id, price, balance FROM invoicet WHERE number = %s", (number))
        factura = cursor.fetchone()
    cnn.close
    return factura