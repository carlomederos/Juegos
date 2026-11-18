import unittest

from extensions import db
from main import app


class JuegoApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
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

    def crear_juego(self, **cambios):
        datos = {
            'nombre': 'Hades',
            'descripcion': 'Acción y aventura',
            'precio': 299.99,
        }
        datos.update(cambios)
        return self.client.post('/api/juegos', json=datos)

    def test_listar_api_vacia(self):
        respuesta = self.client.get('/api/juegos')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json(), {'juegos': []})

    def test_crear_y_obtener_juego(self):
        creado = self.crear_juego()
        self.assertEqual(creado.status_code, 201)
        datos = creado.get_json()
        self.assertEqual(datos['nombre'], 'Hades')
        self.assertEqual(datos['descripcion'], 'Acción y aventura')

        obtenido = self.client.get(f"/api/juegos/{datos['id']}")
        self.assertEqual(obtenido.status_code, 200)
        self.assertEqual(obtenido.get_json()['nombre'], 'Hades')

    def test_rechaza_datos_invalidos(self):
        respuesta = self.client.post('/api/juegos', json={'nombre': 'Sin demás datos'})
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('error', respuesta.get_json())

    def test_actualizar_y_eliminar_juego(self):
        creado = self.crear_juego()
        juego_id = creado.get_json()['id']
        actualizado = self.client.put(
            f'/api/juegos/{juego_id}', json={'precio': 0}
        )
        self.assertEqual(actualizado.status_code, 200)
        self.assertEqual(actualizado.get_json()['precio'], 0)

        eliminado = self.client.delete(f'/api/juegos/{juego_id}')
        self.assertEqual(eliminado.status_code, 204)
        self.assertEqual(self.client.get(f'/api/juegos/{juego_id}').status_code, 404)

    def test_recurso_inexistente_responde_404(self):
        respuesta = self.client.get('/api/juegos/9999')
        self.assertEqual(respuesta.status_code, 404)
        self.assertIn('error', respuesta.get_json())


if __name__ == '__main__':
    unittest.main()
