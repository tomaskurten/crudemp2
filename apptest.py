from flask import Flask
from flaskext.mysql import MySQL
from flask import render_template, request, redirect

app=Flask(__name__)

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
    _nombre=request.form["txtNombre"]
    _correo=request.form["txtCorreo"]
    _foto="null.jpg"
    
    datos=(_nombre,_correo,_foto)
    
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
    # sql="UPDATE `empleados` SET `nombre` = 'editexitoso' WHERE `empleados`.`id` = 12;"
    sql="SELECT * FROM `sistema`.`empleados` WHERE id=12"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    
    conn.commit()
    return render_template("empleados/edit.html")

if __name__=="__main__":
    app.run(debug=True,port=8055)