from flask import render_template
from . import mediamanager

@mediamanager.route('/')
def index():
    return  render_template("mediamanager.html")

@mediamanager.route('/getmedias', methods=["GET"])
def getmedias():
    return  render_template("mediamanager.html")

@mediamanager.route('/addmedia', methods=["POST"])
def addmedia():
    return  render_template("mediamanager.html")

@mediamanager.route('/removemedia', methods=["DELETE"])
def removemedia():
    return  render_template("mediamanager.html")