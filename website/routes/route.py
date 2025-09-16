from flask import send_from_directory
from . import editlogin

# Route to serve uploaded images
@editlogin.route("/images/<path:filename>")
def uploaded_images(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)