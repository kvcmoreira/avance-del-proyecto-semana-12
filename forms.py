# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired()])