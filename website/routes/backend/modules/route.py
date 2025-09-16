from flask import Blueprint, render_template

from .mediamanager.route import mediamanager
from .productmanager.route import productmanager

modules = Blueprint('modules', __name__, url_prefix='/modules')

modules.register_blueprint(mediamanager)
modules.register_blueprint(productmanager)