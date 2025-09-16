from flask import Blueprint, render_template

productmanager = Blueprint('productmanager', __name__, template_folder="templates", url_prefix='/productmanager')

@productmanager.route('/')
def index():
    return  render_template("productmanager.html")