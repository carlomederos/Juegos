from extensions import db

class Juego(db.Model):
    __tablename__ = 'juegos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(9, 2), nullable=False)
