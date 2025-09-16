from website.app import db
from datetime import datetime


class Medias(db.Model):
    __tablename__ = "medias"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    type = db.Column(db.String(16), nullable=True)
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    ext = db.Column(db.String(16), nullable=True)
    create_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    deleted_yn = db.Column(db.Boolean, default=False)

class MediaUsed(db.Model):
    __tablename__ = "mediaused"

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, default=0)
    function_as = db.Column(db.String(250), nullable=True)
    create_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    deleted_yn = db.Column(db.Boolean, default=False)

    '''media_id INTEGER NOT NULL,
            modules_id INTEGER NOT NULL,'''