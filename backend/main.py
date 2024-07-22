from flask import Flask, jsonify, request
from models import db, Dragones, TiposDragon, Granjas, TiposGranja, Almacen
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import atexit

USUARIO = 'tomascrojo'
PASSWORD = '15012004'

app = Flask(__name__)
puerto = 5000
app.config['SQLALCHEMY_DATABASE_URI']= f'postgresql+psycopg2://{USUARIO}:{PASSWORD}@localhost:5432/dragon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

def actualizar():
    try:
        with app.app_context():
            dragones = db.session.query(Dragones).where(Dragones.salud > 0).all()
            for dragon in dragones:

                tiempo_desde_actualizacion = datetime.datetime.now() - dragon.ultima_actualizacion
                minutos_desde_actualizacion = tiempo_desde_actualizacion.total_seconds()//60

                if minutos_desde_actualizacion <= 0:
                    pass

                comida_a_restar = minutos_desde_actualizacion
                
                if comida_a_restar > dragon.hambre:
                    comida_a_restar -= dragon.hambre
                    dragon.hambre = 0
                elif dragon.hambre > 0:
                    dragon.hambre -= comida_a_restar
                    comida_a_restar = 0

                dragon.salud -= comida_a_restar
                dragon.ultima_actualizacion += datetime.timedelta(minutes=minutos_desde_actualizacion)

            db.session.commit()

    except Exception as error:
        print("Error al actualizar:", error)

scheduler = BackgroundScheduler()
scheduler.add_job(actualizar, 'interval', seconds=5)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
        

@app.route("/almacen", methods=['GET'])
def get_almacen():
    try:
        almacen = db.session.query(Almacen).first()

        if not almacen:
            return jsonify({'message': 'Almacen not found'}), 404

        almacen_data = {
            'id' : almacen.id,
            'comida': almacen.comida
        }
        return jsonify(almacen_data)
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/dragones", methods=['GET'])
def get_dragones():
    try:
        dragones = db.session.query(Dragones, TiposDragon
        ).where(Dragones.id_tipo==TiposDragon.id)

        dragones_data = []
        for dragon, tipo_dragon in dragones:
            dragon_data = {
                'id': dragon.id,
                'tipo_dragon': tipo_dragon.nombre,
                'fecha_creacion': dragon.fecha_creacion,
                'nombre': dragon.nombre,
                'salud': dragon.salud,
                'hambre': dragon.hambre,
                'ultima_actualizacion': dragon.ultima_actualizacion
            }
            dragones_data.append(dragon_data)
        return jsonify({'dragones':dragones_data})
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/dragones/<id_dragon>", methods=['GET'])
def get_dragon(id_dragon):
    try:
        data = db.session.query(Dragones, TiposDragon
        ).where(Dragones.id_tipo==TiposDragon.id).where(Dragones.id==id_dragon).first()

        if not data:
            return jsonify({'message': 'Dragon not found'}), 404

        dragon, tipo_dragon = data

        dragon_data = {
            'id': dragon.id,
            'tipo_dragon': tipo_dragon.nombre,
            'fecha_creacion': dragon.fecha_creacion,
            'nombre': dragon.nombre,
            'salud': dragon.salud,
            'hambre': dragon.hambre,
            'ultima_actualizacion': dragon.ultima_actualizacion
        }
        return jsonify(dragon_data)
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/tipos_dragon", methods=['GET'])
def get_tipos_dragon():
    try:
        tipos_dragon = db.session.query(TiposDragon).all()

        tipos_dragon_data = []
        for tipo_dragon in tipos_dragon:
            tipo_dragon_data = {
                'id': tipo_dragon.id,
                'nombre': tipo_dragon.nombre,
                'precio': tipo_dragon.precio,
            }
            tipos_dragon_data.append(tipo_dragon_data)
        return jsonify({'tipos_dragon':tipos_dragon_data})
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/granjas", methods=['GET'])
def get_granjas():
    try:
        granjas = db.session.query(Granjas, TiposGranja
        ).where(Granjas.id_tipo==TiposGranja.id)

        granjas_data = []
        for (granja, tipo_granja) in granjas:
            granja_data = {
                'id': granja.id,
                'tipo_granja': tipo_granja.nombre,
                'fecha_creacion': granja.fecha_creacion,
                'fecha_cosecha': granja.fecha_cosecha,
                'cosechada': granja.cosechada
            }
            granjas_data.append(granja_data)
        return jsonify({'granjas':granjas_data})
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/granjas/<id_granja>", methods=['GET'])
def get_granja(id_granja):
    try:
        data = db.session.query(Granjas, TiposGranja
        ).where(Granjas.id_tipo==TiposGranja.id).where(Granjas.id==id_granja).first()

        granja, tipo_granja = data

        if not data:
            return jsonify({'message': 'Granja not found'}), 404

        granja_data = {
            'id': granja.id,
            'tipo_granja': tipo_granja.nombre,
            'fecha_creacion': granja.fecha_creacion,
            'fecha_cosecha': granja.fecha_cosecha,
            'cosechada': granja.cosechada
        }
        return jsonify(granja_data)
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/tipos_granja", methods=['GET'])
def get_tipos_granja():
    try:
        tipos_granja = db.session.query(TiposGranja).all()

        tipos_granja_data = []
        for tipo_granja in tipos_granja:
            tipo_granja_data = {
                'id': tipo_granja.id,
                'nombre': tipo_granja.nombre,
                'precio': tipo_granja.precio,
                'recompensa': tipo_granja.recompensa,
                'tiempo_cosecha': tipo_granja.tiempo_cosecha
            }
            tipos_granja_data.append(tipo_granja_data)
        return jsonify({'tipos_granja':tipos_granja_data})
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/nuevo_dragon", methods=['POST'])
def add_dragones():
    try:
        id_tipo = request.args.get('id_tipo')
        nombre = request.args.get('nombre')

        if not id_tipo or not nombre:
            return jsonify({'message': 'Bad request, id_tipo or nombre not provided'}), 400
        
        if not TiposDragon.query.where(TiposDragon.id==id_tipo).first():
            return jsonify({'message': f'Bad request, id_tipo={id_tipo} is not a valid value'}), 400
        
        tipo_dragon = TiposDragon.query.get(id_tipo)
        almacen = db.session.query(Almacen).first()

        if almacen.comida < tipo_dragon.precio:
            return jsonify({'message': f'Comida insuficiente'}), 400

        almacen.comida -= tipo_dragon.precio
        
        fecha_creacion = datetime.datetime.now()
        
        nuevo_dragon = Dragones(id_tipo=id_tipo, nombre=nombre, fecha_creacion=fecha_creacion, ultima_actualizacion=fecha_creacion)
        db.session.add(nuevo_dragon)
        db.session.commit()

        return jsonify({'dragon': {'id': nuevo_dragon.id, 'id_tipo': nuevo_dragon.id_tipo, 'fecha_creacion': nuevo_dragon.fecha_creacion, 'nombre': nuevo_dragon.nombre, 'salud': nuevo_dragon.salud, 'hambre': nuevo_dragon.hambre, 'ultima_actualizacion': nuevo_dragon.ultima_actualizacion}}), 201
    
    
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/alimentar/<id_dragon>", methods=['POST'])
def alimentar(id_dragon):
    try:
        str_cantidad_comida = request.args.get('cantidad_comida')
        dragon = db.session.query(Dragones).get(id_dragon)
        almacen = db.session.query(Almacen).first()

        if not dragon:
            return jsonify({'message': 'Dragon not found'}), 404
        
        if not str_cantidad_comida:
            return jsonify({'message': 'Bad request, cantidad_comida not provided'}), 400
        
        if not str_cantidad_comida.isnumeric():
            return jsonify({'message': f'Bad request, cantidad_comida debe ser un numero'}), 400
        
        cantidad_comida = int(str_cantidad_comida)

        if cantidad_comida <= 0:
            return jsonify({'message': f'cantidad_comida debe ser mayor a 0'}), 400

        if almacen.comida < cantidad_comida:
            return jsonify({'message': f'Comida insuficiente'}), 400

        almacen.comida -= cantidad_comida
        dragon.hambre += cantidad_comida
        
        db.session.commit()

        return jsonify({'dragon': {'id': dragon.id, 'id_tipo': dragon.id_tipo, 'fecha_creacion': dragon.fecha_creacion, 'nombre': dragon.nombre, 'salud': dragon.salud, 'hambre': dragon.hambre, 'ultima_actualizacion': dragon.ultima_actualizacion}}), 201
    
    
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/nueva_granja", methods=['POST'])
def add_granjas():
    try:
        id_tipo = request.args.get('id_tipo')

        if not id_tipo:
            return jsonify({'message': 'Bad request, id_tipo not provided'}), 400
        
        if not TiposGranja.query.where(TiposGranja.id==id_tipo).first():
            return jsonify({'message': f'Bad request, id_tipo={id_tipo} is not a valid value'}), 400
        
        tipo_granja = TiposGranja.query.get(id_tipo)
        almacen = db.session.query(Almacen).first()

        if almacen.comida < tipo_granja.precio:
            return jsonify({'message': f'Comida insuficiente'}), 400
        
        almacen.comida -= tipo_granja.precio

        fecha_creacion = datetime.datetime.now()
        fecha_cosecha = fecha_creacion + datetime.timedelta(minutes=tipo_granja.tiempo_cosecha)
        
        nueva_granja = Granjas(id_tipo=id_tipo, fecha_creacion=fecha_creacion, fecha_cosecha=fecha_cosecha)
        db.session.add(nueva_granja)
        db.session.commit()

        return jsonify({'granja': {'id': nueva_granja.id, 'id_tipo': nueva_granja.id_tipo, 'fecha_creacion': nueva_granja.fecha_creacion, 'fecha_cosecha': nueva_granja.fecha_cosecha, 'cosechada': nueva_granja.cosechada}}), 201
    
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/cosechar/<id_granja>", methods=['POST'])
def cosechar_granja(id_granja):
    try:
        if not id_granja:
            return jsonify({'message': 'Bad request, id_granja not provided'}), 400
        
        data = db.session.query(Granjas, TiposGranja
        ).where(Granjas.id_tipo==TiposGranja.id).where(Granjas.id==id_granja).first()

        granja, tipo_granja = data
        almacen = db.session.query(Almacen).first()

        
        if not data:
            return jsonify({'message': f'Granja not found'}), 404
        
        if granja.cosechada:
            return jsonify({'message': f'Granja ya cosechada'}), 400 

        if datetime.datetime.now() < granja.fecha_cosecha:
            return jsonify({'message': f'Granja no lista para cosecha'}), 400
        
        if not almacen:
            return jsonify({'message': 'Almacen not found'}), 404
        
        granja.cosechada = True
        almacen.comida += tipo_granja.recompensa

        db.session.commit()

        return jsonify({'granja': {'id': granja.id, 'id_tipo': granja.id_tipo, 'fecha_creacion': granja.fecha_creacion, 'fecha_cosecha': granja.fecha_cosecha, 'cosechada': granja.cosechada}}), 201
    
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, use_reloader=False, port=puerto)