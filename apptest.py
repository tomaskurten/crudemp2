from flask import Flask
from flaskext.mysql import MySQL
from datetime import datetime
from flask import render_template, request,redirect, send_from_directory
import os

app=Flask(__name__)
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

mysql=MySQL()
# Creamos la referencia al host, para que se conecte a la base
# de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_HOST']='localhost'
# Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_USER']='root'
# Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_PASSWORD']=''
# Nombre de nuestra BD
app.config['MYSQL_DATABASE_BD']='sistema' 

mysql.init_app(app) 

@app.route('/')
def index():
    sql="SELECT * FROM `sistema`.`empleados`"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    db_empleados=cursor.fetchall()
    for empleado in db_empleados:
        print(empleado)
    # conn.commit()
    return render_template("empleados/index.html",empleados=db_empleados)

@app.route("/create")
def create():
    return render_template("empleados/create.html")

@app.route("/store",methods=["POST"])
def storage():
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    _nombre=request.form["txtNombre"]
    _correo=request.form["txtCorreo"]
    _foto=request.files["txtFoto"]
    
    if _foto.filename!="":
        nombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nombreFoto)
    
    datos=(_nombre,_correo,nombreFoto)
    
    sql="INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route("/destroy/<int:id>")
def destroy(id):
    sql="DELETE FROM `sistema`.`empleados` WHERE `empleados`.`id` = %s"
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,(id))
    conn.commit()
    return redirect('/')

@app.route("/edit/<int:id>")
def edit(id):
    sql="SELECT * FROM `sistema`.`empleados` WHERE `empleados`.`id` = %s"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,(id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template("empleados/edit.html", empleados=empleados)


@app.route("/update",methods=["POST"])
def update():
    _nombre=request.form["txtNombre"]
    _correo=request.form["txtCorreo"]
    # _foto="null.jpg"
    id=request.form["txtID"]
    sql="UPDATE `sistema`.`empleados` SET `nombre` = %s, `correo` = %s WHERE `empleados`.`id` = %s;"
    datos=(_nombre,_correo,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect("/")

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

if __name__=="__main__":
    app.run(debug=True,port=8055)