from . import *

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