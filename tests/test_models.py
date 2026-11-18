import unittest

import controllers
from extensions import db
from main import app
from models import Juego


class JuegoModelTests(unittest.TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_crear_juego_y_validar_campos(self):
        juego = Juego(nombre='Portal 2', descripcion='Puzles', precio=199.90)
        db.session.add(juego)
        db.session.commit()

        guardado = db.session.get(Juego, juego.id)
        self.assertIsNotNone(guardado)
        self.assertEqual(guardado.nombre, 'Portal 2')
        self.assertEqual(guardado.descripcion, 'Puzles')
        self.assertEqual(float(guardado.precio), 199.90)

    def test_controladores_actualizan_y_eliminan_juego(self):
        controllers.insertar_juego('Celeste', 'Plataformas', 150)
        juego = Juego.query.one()

        controllers.actualizar_juego('Celeste', 'Aventura', 175, juego.id)
        actualizado = controllers.obtener_juego_por_id(juego.id)
        self.assertEqual(actualizado.descripcion, 'Aventura')
        self.assertEqual(float(actualizado.precio), 175.0)

        controllers.eliminar_juego(juego.id)
        self.assertEqual(Juego.query.count(), 0)

    def test_modelo_rechaza_nombre_nulo(self):
        db.session.add(Juego(nombre=None, descripcion='Sin nombre', precio=10))
        with self.assertRaises(Exception):
            db.session.commit()
        db.session.rollback()


if __name__ == '__main__':
    unittest.main()
