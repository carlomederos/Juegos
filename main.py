from flask import Flask, render_template, request, redirect
from flask_login import login_required
from extensions import db, login_manager
from models import Juego
import controllers
from auth import auth
from api import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')

app.config['SECRET_KEY'] = '7eb18fe65189d94ac4494ccd1a76178ba01ed27585bcd48aac48dd33d8d73328'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:carlo2005@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
@app.route('/juegos')
@login_required
def juegos():
    juegos = controllers.obtener_juegos()
    return render_template('juegos.html', juegos=juegos)

@app.route('/agregar_juego.html')
@login_required
def formulario_agregar_juego():
    return render_template('agregar_juego.html')

@app.route('/guardar_juego', methods=['POST'])
@login_required
def guardar_juego():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']

    controllers.insertar_juego(
        nombre, descripcion, precio
        )
    return redirect('/juegos')

@app.route('/eliminar_juego', methods=['POST'])
@login_required
def eliminar_juego():
    id = request.form['id']
    controllers.eliminar_juego(id)

    return redirect('/juegos')

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)

    return render_template(
        'editar_juego.html', 
        juego=juego
    )

@app.route('/actualizar_juego', methods=['POST'])
@login_required
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
