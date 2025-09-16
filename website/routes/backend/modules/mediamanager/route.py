import os
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
from . import mediamanager, ALLOWED_EXTENSIONS, UPLOAD_ROOT

#routes
@mediamanager.route('/')
def index():
    return  render_template("mediamanager.html")

@mediamanager.route('/getmedias', methods=["GET"])
def getmedias():
    
    if request.method == "GET":
        medias = [
            {"id": 1, "name": "img1", "path": "/static/images/img1/thumbs.png"},
            {"id": 2, "name": "img2", "path": "/static/images/img2/thumbs.jpg"}
        ]
        return jsonify(medias)

@mediamanager.route('/addmedia', methods=["POST"])
def addmedia():
    
    if request.method == "POST":
        if "images" not in request.files:
            return jsonify({"status": "error", "message": "No images found"}), 400
        
        files = request.files.getlist("images")
        
        if not files:
            return jsonify({"status": "error", "message": "Empty file list"}), 400

        invalidfilesfound = any( not file or not allowed_file(file.filename) for file in files)
        #print(invalidfilesfound)

        if invalidfilesfound:
             return jsonify({"status": "error", "message": "An unsupport file was found"}), 400
        
        for file in files:
            ext = os.path.splitext(file.filename)[1].lower()
            name = os.path.splitext(file.filename)[0]
            base_name =( secure_filename(name) or "iamge")

            upload_folder = create_unique_folder(base_name) 

            filename = f"image{ext}"
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path) 
        
        return jsonify({"status": "success", "message": "images are uploaded"}), 200

@mediamanager.route('/removemedia', methods=["DELETE"])
def removemedia():
    print("heloo")
    if request.method == "DELETE":
        data = request.get_json()  # Get the JSON body
        media_id = data.get("id")  # Access your id
        return jsonify({"status": "success", "message": "images are removes"}), 200
    return jsonify({"status": "error", "message": "Not Supported"}), 400


#function 
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def create_unique_folder(base_name="image"):
    folder_path = os.path.join(UPLOAD_ROOT, base_name)
    counter = 1

    while os.path.exists(folder_path):
        folder_path = os.path.join(UPLOAD_ROOT, f"{base_name}({counter})")
        counter += 1
       
    os.makedirs(folder_path, exist_ok=True)
    return folder_path