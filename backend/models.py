from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Almacen(db.Model):
    __tablename__ = 'almacen'
    id = db.Column(db.Integer, primary_key=True)
    comida = db.Column(db.Integer, default=50)

class TiposDragon(db.Model):
    __tablename__ = 'tipos_dragon'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Integer, nullable=False)

class Dragones(db.Model):
    __tablename__ = 'dragones'
    id = db.Column(db.Integer, primary_key=True)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos_dragon.id'), nullable=False)
    fecha_creacion = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    salud = db.Column(db.Integer, nullable=False, default=100)
    hambre = db.Column(db.Integer, nullable=False, default=100)
    ultima_actualizacion = db.Column(db.Integer, nullable=False)

class TiposGranja(db.Model):
    __tablename__ = 'tipos_granja'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    recompensa = db.Column(db.Integer, nullable=False)
    tiempo_cosecha = db.Column(db.Integer, nullable=False)

class Granjas(db.Model):
    __tablename__ = 'granjas'
    id = db.Column(db.Integer, primary_key=True)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos_granja.id'), nullable=False)
    fecha_creacion = db.Column(db.Integer, nullable=False)
    fecha_cosecha = db.Column(db.Integer, nullable=False)
    cosechada = db.Column(db.Boolean, nullable=False, default=False)