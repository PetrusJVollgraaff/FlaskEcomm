from website.app import db
from sqlalchemy import text
from flask import Blueprint, redirect, render_template, url_for

from .products.route import productpages
from .cart.route import cartpages

views = Blueprint('views', __name__, template_folder="templates")

views.register_blueprint(productpages)
views.register_blueprint(cartpages)

@views.route('/')
def index():
    return  render_template("home.html")