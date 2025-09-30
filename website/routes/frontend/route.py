from . import * 

views.register_blueprint(productpages)
views.register_blueprint(cartpages)

@views.route('/')
def index():
    return  render_template("home.html")