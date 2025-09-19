import os
from website.app import db
from flask import Blueprint,jsonify, render_template, request
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from datetime import date, timedelta

mindate = date.today()+ timedelta(days=1)
#Product Create/Edit Form
class ProductForm(FlaskForm):
    
    product_id = IntegerField("Product id", validators=[NumberRange(min=0)])
    product_name = StringField("Product Name", validators=[DataRequired(), Length(1,200)])
    product_code = StringField("Product Code", validators=[DataRequired(), Length(1,200)])
    product_decription = TextAreaField("Product Description")
    product_stock = IntegerField("Product in stock", validators=[DataRequired(), NumberRange(min=0)])
    product_show = BooleanField("Show on site")
    product_special = BooleanField("Product on special")

    price_normal = FloatField('Price', validators=[InputRequired(), NumberRange(min=0)], render_kw={"type" : "number"}, default=0)
    price_special = FloatField('Special Price', validators=[NumberRange(min=0)], render_kw={"type" : "number"}, default=0)
    special_datestart = DateField("Special Date Start", format="%Y-%m-%d", default=mindate, render_kw={"min" : mindate })
    special_dateend = DateField("Special Date End", format="%Y-%m-%d", default=date.today()+ timedelta(days=3), render_kw={"min" : mindate + timedelta(days=1)})
    
    #main_imgid = IntegerField("Product id", validators=[InputRequired(), NumberRange(min=0)])


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

#Get the html
@productmanager.route('/', methods=["GET"])
def index():
    return  render_template("productmanager.html")

#Get availible products
@productmanager.route('/getproducts', methods=["GET"])
def getproducts():
    if request.method == "GET":
        sql = text("""
                    SELECT 
                        P.id, 
                        P.name, 
                        P.onspecial,
                        P.showonline,
                        CASE 
                            WHEN M.id IS NOT NULL THEN
                                '/static/images/'|| M.name ||'/thumb'|| M.ext
                            ELSE ''
                        END AS path 

                    FROM products AS P
                    LEFT JOIN mediaused MU ON MU.id = P.mediaused_id AND MU.deleted_yn=0
                    LEFT JOIN medias M ON M.id = MU.media_id AND M.deleted_yn=0
                    WHERE P.deleted_yn = 0 
                """)
        result = db.session.execute(sql)
        results = result.mappings().all()
        
        products = []
        for row in results:
            products.append({
                "id": row["id"],
                "name": row["name"],
                "onspecial": row["onspecial"],
                "showonline": row["showonline"],
                "image": {
                    "path": row["path"]
                }
            })

        return jsonify(products)


#Mark product as delete
@productmanager.route('/removeproduct', methods=["DELETE"])
def removeproduct():
    
    if request.method == "DELETE":
        data = request.get_json()  # Get the JSON body
        product_id = data.get("id")  # Access your id
        return jsonify({"status": "success", "message": "product are removes"}), 200
       
    return jsonify({"status": "error", "message": "Not Supported"}), 400


#Create a new product
@productmanager.route("/productfield", methods=["GET", "POST"])
def productAdd():
    form = ProductForm()
        
    if request.method == 'POST':
        if not form.validate_on_submit():
            return jsonify({ "status": "error", "message": "Product could not be created", "reason": form.errors }), 500
        
        sqlimg = text('''
                INSERT INTO mediaused ([media_id], [order], [function_as], [create_at], [deleted_yn])
                VALUES (:imgid, 0, "main product image", CURRENT_TIME, 0)
                RETURNING id;
            ''')

        result = db.session.execute(sqlimg, {"imgid": 1})
        row_mediaused = result.fetchone()
        db.session.commit()
    
        sqlproduct = text('''
                        INSERT INTO products([mediaused_id], [name], [instock], [description], [code], [onspecial], [showonline], [create_at], [deleted_yn])
                        VALUES (:imgusedid, :name, :instock, :descript, :code, :onspecial, :showonline, CURRENT_TIME, 0)
                          RETURNING id;
                    ''')

        result = db.session.execute(sqlproduct, 
                                    {
                                        "imgusedid": row_mediaused.id, 
                                        "name": form.product_name.data,
                                        "descript": form.product_decription.data,
                                        "code": form.product_code.data,  
                                        "instock": form.product_stock.data,
                                        "onspecial": 1 if form.product_special.data else 0,
                                        "showonline": 1 if form.product_show.data else 0,
                                    }
                                    )
        row_product = result.fetchone()
        db.session.commit()                 


        return jsonify({ "status": "success", "message": "product is added" })
    
    return render_template('productform.html', form=form)


#Update/Edit product value
@productmanager.route("/productfield/<int:productid>", methods=["GET", "PUT"])
def productEdit(productid):
    form = ProductForm() 
    sql = text("""
                SELECT 
                    P.id, 
                    P.name, 
                    P.description,
                    P.code,
                    P.instock,
                    P.onspecial,
                    P.showonline,
                    CASE 
                        WHEN M.id IS NOT NULL THEN
                            '/static/images/'|| M.name ||'/thumb'|| M.ext
                        ELSE ''
                    END AS path
                FROM products AS P
                LEFT JOIN mediaused MU ON MU.id = P.mediaused_id AND MU.deleted_yn=0
                LEFT JOIN medias M ON M.id = MU.media_id AND M.deleted_yn=0
                WHERE P.deleted_yn = 0 AND P.id=:productid
            """)
    result = db.session.execute(sql, {"productid": productid})
    results = result.mappings().fetchone()       

    if not results:
        return jsonify({ "status": "error", "message": "product not found" }), 404

    if request.method == 'GET':
        form.product_name.data = results["name"]
        form.product_decription.data = results["description"]
        form.product_code.data = results["code"]
    
        form.product_stock.data = results["instock"]
        form.product_special.data = results["onspecial"] == 1
        form.product_show.data = results["showonline"] == 1   
    
    if request.method == 'PUT':
        if not form.validate_on_submit():
            return jsonify({ "status": "error", "message": "Product could not be updated", "reason": form.errors }), 500
        
        sqlproduct = text('''
                UPDATE products SET [name]=:name, [instock]=:instock, [description]=:descript, [code]=:code, 
                    [onspecial]=:onspecial, [showonline]=:showonline
                WHERE id=:id
                RETURNING id;
            ''')

        result = db.session.execute(sqlproduct, 
                                    {
                                        "id": form.product_id.data, 
                                        "name": form.product_name.data,
                                        "descript": form.product_decription.data,
                                        "code": form.product_code.data,  
                                        "instock": form.product_stock.data,
                                        "onspecial": 1 if form.product_special.data else 0,
                                        "showonline": 1 if form.product_show.data else 0,
                                    }
                                    )
        row_product = result.fetchone()
        db.session.commit()                 
        
        return jsonify({ "status": "success", "message": "product is updated" }), 200
        
    return render_template('productform.html', form=form)