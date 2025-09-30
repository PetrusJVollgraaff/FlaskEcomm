from datetime import timedelta
from website.app import db
import email_validator
from flask import Blueprint,render_template, request,redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email
from website.models.users import User