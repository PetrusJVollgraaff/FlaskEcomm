
from flask import render_template,Blueprint
from flask_login import login_required

from .mediamanager.route import mediamanager
from .productmanager.route import productmanager

modules = Blueprint(
    'modules', __name__, 
    url_prefix='/modules', 
    static_folder='static' 
)