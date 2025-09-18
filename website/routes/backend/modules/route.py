
from flask import render_template,Blueprint
from flask_login import login_required

from .mediamanager.route import mediamanager
from .productmanager.route import productmanager

modules = Blueprint(
    'modules', __name__, 
    url_prefix='/modules', 
    static_folder='static' 
)

#prevent Unautherized user access
@modules.before_request
@login_required
def require_login():
    # This will run before *every* request in this blueprint
    pass

modules.register_blueprint(mediamanager)
modules.register_blueprint(productmanager)

@modules.route('/')
def index():
    return  render_template("dashboard.html")