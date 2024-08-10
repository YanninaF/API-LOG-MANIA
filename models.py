from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicio = db.Column(db.String(50), nullable=True)
    nivel = db.Column(db.String(20), nullable=True)
    mensaje = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
