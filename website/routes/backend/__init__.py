import email_validator
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email


editlogin = Blueprint('editlogin', __name__, template_folder="templates", url_prefix='/edit')

class BackendLoginForm(FlaskForm):
    email = EmailField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

from . import route