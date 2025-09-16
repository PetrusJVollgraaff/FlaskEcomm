import os
from flask import Blueprint,send_from_directory
# Path to uploads folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "website", "uploads", "images")

editlogin = Blueprint('editlogin', __name__, url_prefix='/static')

from . import route

