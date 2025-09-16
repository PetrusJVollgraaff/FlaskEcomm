from flask import Blueprint, redirect, render_template, url_for

views = Blueprint('views', __name__, template_folder="templates")

@views.route('/')
def index():
    return  render_template("home.html")

@views.route('/pages/products')
def products():
    return  render_template("products.html")

@views.route('/pages/products/<int:product_id>')
def product(product_id):
    print(product_id)
    if product_id:
        return  render_template("product.html")
    return  redirect(url_for('views.index'))