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

#Login Form
class BackendLoginForm(FlaskForm):
    email = EmailField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


#route
editlogin = Blueprint('editlogin', __name__, template_folder="templates", url_prefix='/edit')

@editlogin.route('/', methods=["GET", "POST"])
def index():
    loginform = BackendLoginForm()
    
    #if request.method == 'GET':
    #    if(current_user):
    #        return redirect(url_for('modules.index'))
    
    if request.method == 'POST' and loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data
        
        backenduser = User.query.filter_by(email=email).first()

        if backenduser:
            if check_password_hash(backenduser.password, password):
                '''user_log = UserStatusLog( user_id=user.id, status="online")
                db.session.add(user_log)
                db.session.commit()'''
                REMEMBER_COOKIE_DURATION = timedelta(minutes=60)
                
                login_user(backenduser, remember=False, duration=REMEMBER_COOKIE_DURATION)
                loginform.password.data = ''
                return redirect(url_for('modules.index'))

    return  render_template("login.html", form=loginform)

@editlogin.route('/logout')
@login_required
def logout():
    '''user_log = UserStatusLog( user_id=current_user.id, status="offline")
    db.session.add(user_log)
    db.session.commit()'''
    logout_user()
    return redirect(url_for('editlogin.index'))