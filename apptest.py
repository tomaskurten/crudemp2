from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

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
    # return "<h1> HOLA MUNDO!</h1> <p>Adios!</p>"
    sql="INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Bartolo', 'bartolo@mail.com', 'bartolouser.jpg');"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template("empleados/index.html")

if __name__=="__main__":
    app.run(debug=True,port=8055)