from flask import render_template
from . import productmanager

@productmanager.route('/', methods=["GET"])
def index():
    return  render_template("productmanager.html")


@productmanager.route('/getproducts', methods=["GET"])
def getproducts():
    return  render_template("mediamanager.html")

@productmanager.route('/getproduct', methods=["GET"])
def getproduct():
    return  render_template("mediamanager.html")

@productmanager.route('/addproduct', methods=["POST"])
def addproduct():
    return  render_template("mediamanager.html")

@productmanager.route('/removeproduct', methods=["DELETE"])
def removeproduct():
    return  render_template("mediamanager.html")