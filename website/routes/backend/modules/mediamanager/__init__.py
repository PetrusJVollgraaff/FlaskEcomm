import os
from flask_login import current_user
from website.app import db
from sqlalchemy import text
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PIL import Image


UPLOAD_ROOT = os.path.join(os.getcwd(), "website", "public", "images")
os.makedirs(UPLOAD_ROOT, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}

#routes
mediamanager = Blueprint(
    'mediamanager', 
    __name__, 
    template_folder="templates", 
    url_prefix='/mediamanager', 
    static_folder='static'
)