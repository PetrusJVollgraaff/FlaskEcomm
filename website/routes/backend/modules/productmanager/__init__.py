from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import date, timedelta

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#print(BASE_DIR)

productmanager = Blueprint(
    'productmanager', 
    __name__, 
    template_folder="templates", 
    url_prefix='/productmanager',
    static_folder='static'
)

class ProductForm(FlaskForm):

    mindate = date.today()+ timedelta(days=1)

    product_id = IntegerField("Product id", validators=[DataRequired(), NumberRange(min=0)])
    product_name = StringField("Product Name", validators=[DataRequired(), Length(1,200)])
    product_code = StringField("Product Code", validators=[DataRequired(), Length(1,200)])
    product_decription = TextAreaField("Product Description")
    product_stock = IntegerField("Product in stock", validators=[DataRequired(), NumberRange(min=0)])
    product_show = BooleanField("Show on site")
    product_special = BooleanField("Product on special")

    price_normal = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)], render_kw={"type" : "number"})
    price_special = FloatField('Special Price', validators=[NumberRange(min=0)], render_kw={"type" : "number"})
    special_datestart = DateField("Special Date Start", format="%Y/%m/%d", default=mindate, render_kw={"min" : mindate })
    special_dateend = DateField("Special Date End", format="%Y/%m/%d", default=date.today()+ timedelta(days=3), render_kw={"min" : mindate + timedelta(days=1)})
    


from . import route  # Import routes to register them