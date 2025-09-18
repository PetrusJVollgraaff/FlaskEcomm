import os
from flask import Blueprint,send_from_directory
from flask import send_from_directory

# Path to uploads folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "website", "uploads", "images")

editlogin = Blueprint('editlogin', __name__, url_prefix='/static/images')

# Route to serve uploaded images
@editlogin.route("/<path:filename>")
def uploaded_images(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)