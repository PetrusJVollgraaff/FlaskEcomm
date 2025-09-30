import os
from website.app import db
from flask import Blueprint,jsonify, render_template, request
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from datetime import date, timedelta

mindate = date.today()+ timedelta(days=1)

productmanager = Blueprint(
    'productmanager', 
    __name__, 
    template_folder="templates", 
    url_prefix='/productmanager',
    static_folder='static'
)