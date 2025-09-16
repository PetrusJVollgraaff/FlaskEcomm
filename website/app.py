from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "public", "images")

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "supersecretkey"
    
     # Initialize DB and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # 5 MB limit (like multer)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  
    
    from .routes.frontend.route import views
    from .routes.backend.route import editlogin
    from .routes.backend.modules.route import modules

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(editlogin)
    app.register_blueprint(modules)

    @app.route("/static/images/<path:filename>")
    def uploaded_images(filename ):
        return send_from_directory(UPLOAD_FOLDER, filename)

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