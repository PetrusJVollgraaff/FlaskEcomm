from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "supersecretkey"
    
     # Initialize DB and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.frontend.route import views

    app.register_blueprint(views, url_prefix='/')

    # Import models
    from website.models import products, media, modules

    ErrorPage(app)

    return app


def ErrorPage(app):
    #invalid url
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    #internal server error
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500