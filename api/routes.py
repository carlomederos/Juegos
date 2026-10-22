
from flask import request
from flask_restful import Resource
from extensions import db
from models import Juego
from api import api


def juego_a_json(juego):
    return {
        'id': juego.id,
        'nombre': juego.nombre,
        'descripcion': juego.descripcion,
        'precio': float(juego.precio)
    }


def validar_datos(data, parcial=False):
    if not isinstance(data, dict):
        return None, 'Se requiere un objeto JSON válido.'

    permitidos = {'nombre', 'descripcion', 'precio'}
    desconocidos = set(data.keys()) - permitidos

    if desconocidos:
        return None, 'Hay campos no permitidos: ' + ', '.join(sorted(desconocidos))

    if parcial and not data:
        return None, 'Debes enviar al menos un campo para actualizar.'

    if not parcial:
        faltantes = permitidos - set(data.keys())
        if faltantes:
            return None, 'Faltan campos obligatorios: ' + ', '.join(sorted(faltantes))

    resultado = {}

    for campo in ('nombre', 'descripcion'):
        if campo in data:
            valor = data[campo]

            if not isinstance(valor, str) or not valor.strip():
                return None, f'El campo {campo} debe ser un texto no vacío.'

            resultado[campo] = valor.strip()

    if 'precio' in data:
        valor = data['precio']

        if isinstance(valor, bool):
            return None, 'El precio debe ser un número válido.'

        try:
            precio = float(valor)
        except (TypeError, ValueError):
            return None, 'El precio debe ser un número válido.'

        import math

        if not math.isfinite(precio) or precio < 0:
            return None, 'El precio debe ser un número válido mayor o igual a cero.'

        resultado['precio'] = precio

    return resultado, None


class JuegoList(Resource):
    def get(self):
        juegos = Juego.query.order_by(Juego.id).all()
        return {'juegos': [juego_a_json(juego) for juego in juegos]}, 200

    def post(self):
        data, error = validar_datos(request.get_json(silent=True))

        if error:
            return {'error': error}, 400

        juego = Juego(**data)
        db.session.add(juego)
        db.session.commit()

        return juego_a_json(juego), 201


class JuegoResource(Resource):
    def get(self, id):
        juego = db.session.get(Juego, id)

        if juego is None:
            return {'error': 'Videojuego no encontrado.'}, 404

        return juego_a_json(juego), 200

    def put(self, id):
        juego = db.session.get(Juego, id)

        if juego is None:
            return {'error': 'Videojuego no encontrado.'}, 404

        data, error = validar_datos(
            request.get_json(silent=True),
            parcial=True
        )

        if error:
            return {'error': error}, 400

        for campo, valor in data.items():
            setattr(juego, campo, valor)

        db.session.commit()

        return juego_a_json(juego), 200

    def delete(self, id):
        juego = db.session.get(Juego, id)

        if juego is None:
            return {'error': 'Videojuego no encontrado.'}, 404

        db.session.delete(juego)
        db.session.commit()

        return '', 204

api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')