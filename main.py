from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from confidb import get_conexion
import controladorSes, controladorCus, controladorInv
from werkzeug.utils import secure_filename, send_from_directory

app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['UPLOAD_FOLDER'] = 'static/images'
mysql = MySQL(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'invoice'



@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        account = controladorSes.iniciar_log(email, password)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['email'] = account[2]
            return redirect(url_for('home'))
        else:
            msg = 'Correo o Contraseña incorrectas'
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'photo' in request.files:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        account1 = controladorSes.register_log(name)
        if account1:
            msg = 'La cuenta ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Dirección de Correo Electrónico invalida!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'El nombre de usuario solamente debe contener palabras y numeros!'
        elif not name or not email or not password or not photo:
            msg = 'Por favor, rellenar el formulario!'
        else:
            controladorSes.busc_datos(name, email, password, photo)
            msg = 'Se ha registrado correctamente!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Por favor, rellenar el formulario!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    

@app.route('/home')
def home():
    if 'email' in session:
        email = session['email']
        print(email)
    else:
        return redirect(url_for('login'))
    if 'loggedin' in session:
        return render_template('home.html', email=session['email'])
    return redirect(url_for('login'))




@app.route('/indexCli')
def indexCli():
    customers = controladorCus.get_clientes()
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('indexCli.html', customers=customers, account=account)
    return redirect(url_for('login'))

@app.route('/form_add_cliente')
def form_add_cliente():
    return render_template('add_cliente.html')

@app.route('/edit_cliente<int:id>')
def edit_cliente(id):
    customer = controladorCus.get_cliente_id(id)
    return render_template('edit_cliente.html', customer=customer)

@app.route('/update_cliente', methods=['POST'])
def update_cliente():
    id = request.form['id']
    name = request.form['name']
    status = request.form['status']
    mobile = request.form['mobile']
    controladorCus.update_cliente(name, status, mobile, id)
    return redirect('/indexCli')    

@app.route('/delete_cliente', methods=["POST"])
def delete_cliente():
    controladorCus.delete_cliente(request.form["id"])
    return redirect("/indexCli")

@app.route("/save_cliente", methods=["POST"])
def save_cliente():
    name = request.form['name']
    status = request.form['status']
    mobile = request.form['mobile']
    controladorCus.add_cliente(name, status, mobile)
    return redirect("/indexCli")











@app.route('/indexFac')
def indexFac():
    facturas = controladorInv.get_facturas()
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('indexFac.html', facturas=facturas, account=account)
    return redirect(url_for('login'))

@app.route('/form_add_factura')
def form_add_factura():
    return render_template('add_factura.html')

@app.route('/save_factura', methods=['POST'])
def save_factura():
    date = request.form["date"]
    id = request.form["id"]
    price = request.form["price"]
    balance = request.form["balance"]
    controladorInv.add_factura(date, price, balance, id)
    return redirect("/indexFac")

@app.route('/edit_factura/<int:number>')
def edit_factura(number):
    factura = controladorInv.get_facturas_number(number)
    return render_template('edit_factura.html', factura=factura)

@app.route('/update_factura', methods=['POST'])
def update_factura():
    number = request.form["number"]
    date = request.form["date"]
    price = request.form["price"]
    balance = request.form["balance"]
    controladorInv.update_factura(date, price, balance, number)
    return redirect("/indexFac")

@app.route('/delete_factura', methods=["POST"])
def delete_factura():
    balance = request.form['balance']
    balances = int(balance)
    if balances == 0:
        controladorInv.delete_factura(request.form["number"])
    else:
        return ("No se pudo eliminar la factura por el saldo")
    return redirect("/indexFac")



if __name__ == "__main__":
    app.run(port = 2500, debug=True)