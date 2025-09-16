from flask import Blueprint, render_template

editlogin = Blueprint('editlogin', __name__, template_folder="templates", url_prefix='/edit')

@editlogin.route('/')
def index():
    return  render_template("login.html")