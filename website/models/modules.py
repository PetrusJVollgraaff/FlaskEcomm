from website.app import db
from datetime import datetime


class Modules(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    create_at = db.Column(db.DateTime(timezone=True), default=datetime.now())