from website.app import db
from datetime import datetime


class Products(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    mediaused_id = db.Column(db.Integer, db.ForeignKey('mediaused.id'))
    name = db.Column(db.String(250), nullable=False, unique=True)
    instock = db.Column(db.Integer, default=0)
    desciption = db.Column(db.Text, nullable=True)
    code = db.Column(db.String(250), nullable=False)
    onspecial = db.Column(db.Boolean, default=False)
    showonline = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    deleted_yn = db.Column(db.Boolean, default=False)
    
    '''create_by_userid INTEGER NOT NULL,
    deleted_by_userid INTEGER DEFAULT NULL'''

class ProductPrice(db.Model):
    __tablename__ = "productprice"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.Float, nullable=False, default=0.0)
    isspecial = db.Column(db.Boolean, default=False)
    specialdateStart = db.Column(db.DateTime(timezone=True), nullable=True)
    specialdateEnd = db.Column(db.DateTime(timezone=True), nullable=True)
    create_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    deleted_yn = db.Column(db.Boolean, default=False)