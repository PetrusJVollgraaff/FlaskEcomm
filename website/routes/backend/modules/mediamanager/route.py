import os
from flask_login import current_user
from website.app import db
from sqlalchemy import text
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PIL import Image


UPLOAD_ROOT = os.path.join(os.getcwd(), "website", "public", "images")
os.makedirs(UPLOAD_ROOT, exist_ok=True)

#print(BASE_DIR)

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

@mediamanager.route('/')
def index():
    return  render_template("mediamanager.html")

@mediamanager.route('/getmedias', methods=["GET"])
def getmedias():
    if request.method == "GET":
        sql = text("""
                    SELECT 
                        id, 
                        name, 
                        '/static/images/'|| name ||'/thumb'|| ext AS path 
                    FROM medias 
                    WHERE deleted_yn =0""")
        result = db.session.execute(sql)
        results_as_dict = [dict(row) for row in result.mappings()]
        return jsonify(results_as_dict)

@mediamanager.route('/addmedia', methods=["POST"])
def addmedia():
    images = []
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

            upload_folder, name = create_unique_folder(base_name) 

            filename = f"original{ext}"
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path) 

            id = shapeImage(save_path, upload_folder, ext, name)

            images.append(
                {
                    "id" : id,
                    "name": name ,
                    "path" : f"/static/images/{name}/thumb{ext}"
                }
            )
        
        return jsonify({"status": "success", "message": "images are uploaded", "images": images}), 200

@mediamanager.route('/removemedia', methods=["DELETE"])
def removemedia():
    print("heloo")
    if request.method == "DELETE":
        data = request.get_json()  # Get the JSON body
        media_id = data.get("id")  # Access your id
       
        sql = text("""
            UPDATE medias SET deleted_at=CURRENT_TIMESTAMP, deleted_yn=1
            WHERE id=:mediaid
            RETURNING id;
        """)
        result = db.session.execute(sql, {"mediaid": media_id, "userid": current_user.id})
        row = result.fetchone()
        db.session.commit()
       
        return jsonify({"status": "success", "message": "images are removes"}), 200
    return jsonify({"status": "error", "message": "Not Supported"}), 400



#function 
def shapeImage(savedimg, path, ext, name):
    img = Image.open(savedimg)

    sql = text("""
        INSERT INTO medias (name, type, width, height, ext, create_at, deleted_yn)
        VALUES (:name, :type, :width, :height, :ext, CURRENT_TIMESTAMP, 0)
        RETURNING id;
        """)
    result = db.session.execute(sql, {"name": name, "type": "image", "width":img.width, "height":img.height, "ext": ext})
    row = result.fetchone()
    db.session.commit()

    sizes = {
        "default": img.size,
        "large": (1920, int(img.height * 1920/img.width)),
        "medium": (600, int(img.height * 600/img.width)),
        "thumb": (150, 150)
    }

    for key, size in sizes.items():
        img_copy = img.copy()
        if key == "thumb":
            img_copy.thumbnail(size)
        else:
            img_copy = img_copy.resize(size, Image.Resampling.LANCZOS)

        filename = f"{key}{ext}"
        save_path = os.path.join(path, filename)
        img_copy.save(save_path)
     
    return row.id

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def create_unique_folder(base_name="image"):
    name = base_name
    folder_path = os.path.join(UPLOAD_ROOT, name)
    counter = 1

    while os.path.exists(folder_path):
        name = f"{base_name}({counter})"
        folder_path = os.path.join(UPLOAD_ROOT, name)
        counter += 1
       
    os.makedirs(folder_path, exist_ok=True)
    return folder_path, name