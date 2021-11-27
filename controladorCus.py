from confidb import get_conexion

def add_cliente(name, status, mobile):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute("INSERT INTO customer (name, status, mobile) VALUES (%s,%s,%s)",(name,status,mobile))
    cnn.commit()
    cnn.close()

def update_cliente(name, status, mobile, id):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute("UPDATE customer SET name = %s, status = %s, mobile = %s WHERE id = %s", (name, status, mobile, id)) 
    cnn.commit()   
    cnn.close()

def delete_cliente(id):
    cnn = get_conexion()
    with cnn.cursor() as cursor:
        cursor.execute("DELETE FROM customer WHERE id = %s", (id))
    cnn.commit()
    cnn.close()

def get_clientes():
    cnn = get_conexion()
    customer = []
    with cnn.cursor() as cursor:
        cursor.execute("SELECT id, name, status, mobile FROM customer")
        customer = cursor.fetchall()
    cnn.close()
    return customer

def get_cliente_id(id):
    cnn = get_conexion()
    customer = None
    with cnn.cursor() as cursor:
        cursor.execute("SELECT id, name, status, mobile FROM customer WHERE id = %s", (id))
        customer = cursor.fetchone()
    cnn.close()
    return customer