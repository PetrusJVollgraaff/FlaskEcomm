import os
from website.app import db
from flask import Blueprint,jsonify, render_template, request
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import date, timedelta

class ProductForm(FlaskForm):

    mindate = date.today()+ timedelta(days=1)

    product_id = IntegerField("Product id", validators=[DataRequired(), NumberRange(min=0)])
    product_name = StringField("Product Name", validators=[DataRequired(), Length(1,200)])
    product_code = StringField("Product Code", validators=[DataRequired(), Length(1,200)])
    product_decription = TextAreaField("Product Description")
    product_stock = IntegerField("Product in stock", validators=[DataRequired(), NumberRange(min=0)])
    product_show = BooleanField("Show on site")
    product_special = BooleanField("Product on special")

    price_normal = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)], render_kw={"type" : "number"})
    price_special = FloatField('Special Price', validators=[NumberRange(min=0)], render_kw={"type" : "number"})
    special_datestart = DateField("Special Date Start", format="%Y/%m/%d", default=mindate, render_kw={"min" : mindate })
    special_dateend = DateField("Special Date End", format="%Y/%m/%d", default=date.today()+ timedelta(days=3), render_kw={"min" : mindate + timedelta(days=1)})
    

products = [
  {
    "id": 1, "name": "Product One", "image": { "id": 1, "path": "/static/images/img1/thumbs.png"},
  },
  {
    "id": 2, "name": "Product Two", "image": { "id": 2, "path": "/static/images/img2/thumbs.jpg",},
  },
]

#route
productmanager = Blueprint(
    'productmanager', 
    __name__, 
    template_folder="templates", 
    url_prefix='/productmanager',
    static_folder='static'
)


@productmanager.route('/', methods=["GET"])
def index():
    return  render_template("productmanager.html")


@productmanager.route('/getproducts', methods=["GET"])
def getproducts():
    if request.method == "GET":
        sql = text("""
                    SELECT 
                        P.id, 
                        P.name, 
                        P.onspecial,
                        P.showonline,
                        img
                    FROM products P
                    WHERE P.deleted_yn = 0 
                    OUTER APPLY(
                        SELECT 
                            M.id AS 'imgid', 
                            MU.id AS 'imgusedid',
                            '/static/images/'|| M.name ||'/thumb'|| M.ext AS path 
                        FROM mediaused MU
                        JOIN medias M ON M.id = MU.media_id
                        WHERE M.deleted_yn=0 AND MU.deleted_yn=0 AND MU.id = P.mediaused_id 
                   )img   
                   
                """)
        #result = db.session.execute(sql)
        #results_as_dict = [dict(row) for row in result.mappings()]
        
        return jsonify(products)

@productmanager.route('/getproduct', methods=["POST"])
def getproduct():
    if request.method == "POST":
        data = request.get_json()  # Get the JSON body
        product_id = data.get("id")  # Access your id

        product = next((obj for obj in products if obj["id"] == product_id), None)

        if product:
            return jsonify({ "status": "success", "product": product })
        else:
            return jsonify({ "status": "error", "message": "Product not found." })

    return jsonify({ "status": "error", "message": "Something went wrong." })

@productmanager.route('/addproduct', methods=["POST"])
def addproduct():
    return  render_template("mediamanager.html")

@productmanager.route('/removeproduct', methods=["DELETE"])
def removeproduct():
    
    if request.method == "DELETE":
        data = request.get_json()  # Get the JSON body
        product_id = data.get("id")  # Access your id
        return jsonify({"status": "success", "message": "product are removes"}), 200
       
    return jsonify({"status": "error", "message": "Not Supported"}), 400

@productmanager.route("/productfield", methods=["GET", "POST"])
def productAdd():
    form = ProductForm()
        
    if request.method == 'POST':
        productname= form.product_name.data
        productdescript= form.product_decription.data

        print(productname)
        print(productdescript)

        return jsonify({ "status": "success", "message": "product is added" })
    
    return render_template('productform.html', form=form)

@productmanager.route("/productfield/<int:productid>", methods=["GET", "PUT"])
def productEdit(productid):
    form = ProductForm() 
    print(productid)           
    if request.method == 'PUT':

        #print(form.validate_on_submit())
        productname= form.product_name.data
        productdescript= form.product_decription.data

        print(productname)
        print(productdescript)

        return jsonify({ "status": "success", "message": "product is updated" })
        

    return render_template('productform.html', form=form)