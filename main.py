# app.py
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'locoartas'
app.config['MYSQL_DB'] = 'contactos'

mysql = MySQL(app)
CORS(app)  # Habilita CORS para toda la aplicación

@app.route('/api/data')
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, apellido,telefono, email FROM contacto")
    data = cur.fetchall()
    result = []
    for row in data:
        content = {'id': row[0], 'nombre': row[1], 'apellido': row[2], 'telefono': row[3], 'email':row[4]}
        result.append(content)

    return jsonify(result)

@app.route('/api/data/<int:id>')
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT id, nombre, apellido, telefono, email FROM contacto WHERE id = {id}")
    data = cur.fetchall()
    content = {}
    for row in data:
        content = {'id': row[0], 'nombre': row[1], 'apellido': row[2], 'telefono': row[3], 'email':row[4]}
    return jsonify(content)

@app.route('/api/data/<int:id>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM `contactos`.`contacto` WHERE (`id` = '{id}');")
    mysql.connection.commit()
    return 'Eliminar cliente'

@app.route("/api/data", methods=['POST'])
@cross_origin()
def createCustomer():
    if 'id' in request.json:
        updateCustomer()
    else:
        createCustomer()
    return 'ok'
    
def createCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `contacto` (`id`, `nombre`, `apellido`, `telefono`, `email`) VALUES (NULL, %s, %s, %s, %s);",
                (request.json['nombre'], request.json['apellido'], request.json['telefono'], request.json['email']))
    mysql.connection.commit()
    return "Cliente guardado"

def updateCustomer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `contacto` SET `nombre` = %s, `apellido` = %s, `telefono` = %s, `email` = %s WHERE `contacto`.`id` = %s;", (request.json['nombre'], request.json['apellido'], request.json['telefono'], request.json['email'], request.json['id']))
    mysql.connection.commit()
    return "Cliente guardado"

if __name__ == '__main__':
    app.run(debug=True)

