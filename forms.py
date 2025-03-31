from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    stock = IntegerField('Stock', default=0)
    precio = FloatField('Precio', validators=[DataRequired()])
    submit = SubmitField('Agregar Producto')
