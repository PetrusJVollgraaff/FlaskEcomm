from flask import Blueprint
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#print(BASE_DIR)

productmanager = Blueprint(
    'productmanager', 
    __name__, 
    template_folder="templates", 
    url_prefix='/productmanager',
    static_folder='static'
)

from . import route  # Import routes to register them