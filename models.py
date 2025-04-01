from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'


# Crear la base de datos
with app.app_context():
    db.create_all()
