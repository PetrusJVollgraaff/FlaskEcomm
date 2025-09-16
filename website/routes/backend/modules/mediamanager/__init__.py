from flask import Blueprint
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#print(BASE_DIR)

mediamanager = Blueprint(
    'mediamanager', 
    __name__, 
    template_folder="templates", 
    url_prefix='/mediamanager', 
    static_folder='static'
)

from . import route  # Import routes to register them