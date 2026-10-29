import json
from flask import Flask, render_template, request, redirect, jsonify, abort
from werkzeug.exceptions import HTTPException
import logging
from logging.handlers import RotatingFileHandler
from flask_login import login_required
from extensions import db, login_manager
from models import Juego
import controllers
from auth import auth
from api import api_bp

app = Flask(__name__)

archivo_log = RotatingFileHandler(
    'errors.log',
    maxBytes=10240,
    backupCount=3,
    encoding='utf-8'
)

archivo_log.setLevel(logging.ERROR)

archivo_log.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[%(pathname)s:%(lineno)d]'
))

app.logger.addHandler(archivo_log)
app.logger.setLevel(logging.ERROR)

app.register_blueprint(api_bp, url_prefix='/api')

app.config['SECRET_KEY'] = '7eb18fe65189d94ac4494ccd1a76178ba01ed27585bcd48aac48dd33d8d73328'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:carlo2005@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

app.register_blueprint(auth, url_prefix='/auth')

def responder_error(error, plantilla=None):
    if request.path.startswith('/api/'):
        respuesta = error.get_response()
        respuesta.data = json.dumps({
            'codigo': error.code,
            'error': error.name,
            'mensaje': error.description
        })
        respuesta.content_type = 'application/json'
        return respuesta

    if plantilla:
        return render_template(plantilla), error.code

    return error

@app.errorhandler(400)
def error_400(error):
    return responder_error(error, '400.html')

@app.errorhandler(404)
def error_404(error):
    return responder_error(error, '404.html')

@app.errorhandler(405)
def error_405(error):
    return responder_error(error, '405.html')

@app.errorhandler(500)
def error_500(error):
    excepcion = getattr(error, 'original_exception', None)

    if excepcion:
        app.logger.error(
            'Excepción no controlada: %s',
            excepcion,
            exc_info=(
                type(excepcion),
                excepcion,
                excepcion.__traceback__
            )
        )
    else:
        app.logger.error('Error interno del servidor: %s', error)

    return responder_error(error, '500.html')

@app.errorhandler(HTTPException)
def error_http_generico(error):
    if request.path.startswith('/api/'):
        respuesta = error.get_response()
        respuesta.data = json.dumps({
            'codigo': error.code,
            'error': error.name,
            'mensaje': error.description
        })
        respuesta.content_type = 'application/json'
        return respuesta

    return error

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

@app.route('/prueba-400')
def prueba_400():
    abort(400, description='Faltan datos en la solicitud')

@app.route('/prueba-500')
def prueba_500():
    resultado = 1 / 0
    return str(resultado)

    
    return redirect('/juegos')

if __name__ == '__main__':
    app.run(debug=False, port=8000)
