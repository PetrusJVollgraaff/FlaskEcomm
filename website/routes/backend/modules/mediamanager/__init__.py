from flask import Blueprint
import os

UPLOAD_ROOT = os.path.join(os.getcwd(), "website", "public", "images")
#print(BASE_DIR)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}

mediamanager = Blueprint(
    'mediamanager', 
    __name__, 
    template_folder="templates", 
    url_prefix='/mediamanager', 
    static_folder='static'
)

from . import route  # Import routes to register them