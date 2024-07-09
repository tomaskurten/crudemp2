from flask import Flask, render_template, request, redirect, send_from_directory
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
import os

# modificar con URL externa de render
DATABASE_URL = "postgresql+psycopg2://test:qOh8Vm8CbSPS0y9efzHBsUCM3uZVvAps@dpg-cq5m435ds78s73d3ngmg-a.oregon-postgres.render.com/test_ingd"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Configuración de Flask
app = Flask(__name__)
CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)

class Empleado(Base):
    __tablename__ = 'empleados'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, index=True)
    foto = Column(String)

Base.metadata.create_all(bind=engine)

@app.before_request
def create_session():
    request.db = SessionLocal()

@app.after_request
def remove_session(response):
    request.db.close()
    return response

@app.route('/')
def index():
    empleados = request.db.query(Empleado).all()
    return render_template("empleados/index.html", empleados=empleados)

@app.route("/create")
def create():
    return render_template("empleados/create.html")

@app.route("/store", methods=["POST"])
def storage():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]

    if _foto:
        nombreFoto = secure_filename(_foto.filename)
        _foto.save(os.path.join(app.config['CARPETA'], nombreFoto))
    else:
        nombreFoto = ""

    empleado = Empleado(nombre=_nombre, correo=_correo, foto=nombreFoto)
    request.db.add(empleado)
    request.db.commit()
    return redirect('/')

@app.route("/destroy/<int:id>")
def destroy(id):
    empleado = request.db.query(Empleado).get(id)
    if empleado:
        request.db.delete(empleado)
        request.db.commit()
    return redirect('/')

@app.route("/edit/<int:id>")
def edit(id):
    empleado = request.db.query(Empleado).get(id)
    return render_template("empleados/edit.html", empleado=empleado)

@app.route("/update", methods=["POST"])
def update():
    _id = request.form["txtID"]
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]

    empleado = request.db.query(Empleado).get(_id)
    if empleado:
        empleado.nombre = _nombre
        empleado.correo = _correo
        if _foto:
            nombreFoto = secure_filename(_foto.filename)
            _foto.save(os.path.join(app.config['CARPETA'], nombreFoto))
            empleado.foto = nombreFoto
        request.db.commit()
    return redirect('/')

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

if __name__ == "__main__":
    app.run(debug=True, port=8055)
