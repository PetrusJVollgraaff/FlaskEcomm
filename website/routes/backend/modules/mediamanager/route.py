from flask import Blueprint, render_template

mediamanager = Blueprint('mediamanager', __name__, template_folder="templates", url_prefix='/mediamanager')

@mediamanager.route('/')
def index():
    return  render_template("mediamanager.html")