
from flask import Flask, request, jsonify
from models import db, Log
from services import cargar_datos, dividir
from datetime import datetime

app = Flask(__name__)

# Configura la URI de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
db.init_app(app)

# Crea las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas
@app.route('/')
def index():
    return "Página de inicio no disponible."

@app.route('/cargar_datos', methods=['GET'])
def cargar_datos_route():
    return cargar_datos()

@app.route('/dividir', methods=['GET'])
def dividir_route():
    return dividir()

# Endpoint para recibir logs en formato JSON
@app.route('/logs', methods=['POST'])
def recibir_logs():
    data = request.json
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    
    servicio = data.get('servicio')
    nivel = data.get('nivel')
    mensaje = data.get('mensaje')
    timestamp = data.get('timestamp')

    if not all([servicio, nivel, mensaje, timestamp]):
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    log = Log(servicio=servicio, nivel=nivel, mensaje=mensaje, timestamp=timestamp)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"mensaje": "Log recibido y almacenado"}), 201

@app.route('/logs', methods=['GET'])
def consultar_logs():
    servicio = request.args.get('servicio')
    nivel = request.args.get('nivel')
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    query = Log.query
    
    if servicio:
        query = query.filter_by(servicio=servicio)
    if nivel:
        query = query.filter_by(nivel=nivel)
    if desde:
        try:
            desde_fecha = datetime.fromisoformat(desde)
            query = query.filter(Log.timestamp >= desde_fecha)
        except ValueError:
            return jsonify({"error": "Formato de fecha 'desde' inválido. Usa el formato ISO 8601."}), 400
    if hasta:
        try:
            hasta_fecha = datetime.fromisoformat(hasta)
            query = query.filter(Log.timestamp <= hasta_fecha)
        except ValueError:
            return jsonify({"error": "Formato de fecha 'hasta' inválido. Usa el formato ISO 8601."}), 400
    
    logs = query.all()
    resultado = [{"id": log.id, "servicio": log.servicio, "nivel": log.nivel, "mensaje": log.mensaje, "timestamp": log.timestamp.isoformat()} for log in logs]
    
    return jsonify(resultado)


# Endpoint para autenticación
@app.before_request #Esta función se ejecuta antes de cada solicitud
def verificar_autenticacion():
    if request.endpoint == 'recibir_logs' and request.method == 'POST':
        token = request.headers.get('Authorization')
        if token != 'password':
            return jsonify({"error": "Token de autenticación inválido"}), 401

if __name__ == '__main__':
    app.run(debug=True)