from website.app import db
from flask import render_template, request,redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from website.models.users import User
from . import editlogin, BackendLoginForm


@editlogin.route('/', methods=["GET", "POST"])

def index():
    loginform = BackendLoginForm()

    if request.method == 'POST' and loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data
        
        backenduser = User.query.filter_by(email=email).first()
        print(backenduser)
        if backenduser:
            if check_password_hash(backenduser.password, password):
                '''user_log = UserStatusLog( user_id=user.id, status="online")
                db.session.add(user_log)
                db.session.commit()'''
                
                login_user(backenduser, remember=False)
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