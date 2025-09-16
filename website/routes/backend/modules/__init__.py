from flask import Blueprint
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#print(BASE_DIR)

from .mediamanager.route import mediamanager
from .productmanager.route import productmanager


modules = Blueprint(
    'modules', __name__, 
    url_prefix='/modules', 
    static_folder='static' 
)

modules.register_blueprint(mediamanager)
modules.register_blueprint(productmanager)

from . import route