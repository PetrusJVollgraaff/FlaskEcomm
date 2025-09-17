from website.app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True) 
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    deleted_yn = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
