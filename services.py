from flask import jsonify
from models import db, Log
import time

def cargar_datos():
    try:
        # Simula un proceso que tarda 3 segundos
        time.sleep(3)
        log = Log(servicio="cargar_datos", nivel="info", mensaje="Datos cargados exitosamente")
        db.session.add(log)
        db.session.commit()
        return jsonify({"mensaje": "Datos cargados exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def dividir():
    try:
        resultado = 1 / 0  # Esto provocará una excepción ZeroDivisionError
        log = Log(servicio="dividir", nivel="error", mensaje="Resultado: " + str(resultado))
        db.session.add(log)
        db.session.commit()
        return jsonify({"resultado": resultado}), 200
    except ZeroDivisionError as e:
        log = Log(servicio="dividir", nivel="error", mensaje="Error de división por cero")
        db.session.add(log)
        db.session.commit()
        return jsonify({"error": "Error de división por cero"}), 500
