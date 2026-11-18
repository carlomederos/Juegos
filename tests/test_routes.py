import unittest

from extensions import db
from main import app
from models import User


class JuegoRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='clave-de-prueba',
        )
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.app_context.pop()

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def iniciar_sesion_de_prueba(self):
        usuario = User(username='estudiante')
        usuario.password = 'ClaveSegura123'
        db.session.add(usuario)
        db.session.commit()
        respuesta = self.client.post(
            '/auth/login',
            data={'username': 'estudiante', 'password': 'ClaveSegura123'},
        )
        self.assertEqual(respuesta.status_code, 302)

    def test_login_y_registro_son_publicos(self):
        self.assertEqual(self.client.get('/auth/login').status_code, 200)
        self.assertEqual(self.client.get('/auth/register').status_code, 200)

    def test_lista_de_juegos_requiere_autenticacion(self):
        respuesta = self.client.get('/juegos')
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/auth/login', respuesta.headers['Location'])

    def test_usuario_autenticado_accede_a_lista_y_formulario(self):
        self.iniciar_sesion_de_prueba()
        self.assertEqual(self.client.get('/juegos').status_code, 200)
        self.assertEqual(self.client.get('/agregar_juego.html').status_code, 200)

    def test_ruta_inexistente_responde_404(self):
        respuesta = self.client.get('/ruta-que-no-existe')
        self.assertEqual(respuesta.status_code, 404)


if __name__ == '__main__':
    unittest.main()

