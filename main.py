from flask import Flask, render_template, request, redirect
import controllers
from extensions import db
from models import Juego

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:carlo2005@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
@app.route('/juegos')
def juegos():
    juegos = controllers.obtener_juegos()
    return render_template('juegos.html', juegos=juegos)

@app.route('/agregar_juego.html')
def formulario_agregar_juego():
    return render_template('agregar_juego.html')

@app.route('/guardar_juego', methods=['POST'])
def guardar_juego():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']

    controllers.insertar_juego(
        nombre, descripcion, precio
        )
    return redirect('/juegos')

@app.route('/eliminar_juego', methods=['POST'])
def eliminar_juego():
    id = request.form['id']
    controllers.eliminar_juego(id)

    return redirect('/juegos')

@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)

    return render_template(
        'editar_juego.html', 
        juego=juego
    )

@app.route('/actualizar_juego', methods=['POST'])
def actualizar_juego():
    id = request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']

    controllers.actualizar_juego(
        nombre, 
        descripcion, 
        precio, 
        id
        )
    
    return redirect('/juegos')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
