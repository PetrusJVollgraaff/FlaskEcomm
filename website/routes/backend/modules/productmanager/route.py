import os
from website.app import db
from flask import Blueprint,jsonify, render_template, request
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from datetime import date, timedelta

mindate = date.today()+ timedelta(days=1)

#########################################
####### Product Create/Edit Form ########
#########################################
class ProductForm(FlaskForm):
    
    product_id = IntegerField("Product id", validators=[InputRequired(), NumberRange(min=0)])
    product_name = StringField("Product Name", validators=[DataRequired(), Length(1,200)])
    product_code = StringField("Product Code", validators=[DataRequired(), Length(1,200)])
    product_decription = TextAreaField("Product Description")
    product_stock = IntegerField("Product in stock", validators=[InputRequired(), NumberRange(min=0)])
    product_show = BooleanField("Show on site")
    product_special = BooleanField("Product on special")
    main_mediaid = IntegerField("Image id", validators=[InputRequired(), NumberRange(min=0)], render_kw={"hidden" : True})

    price_normal = FloatField('Price', validators=[InputRequired(), NumberRange(min=0)], render_kw={"type" : "number"}, default=0)
    price_special = FloatField('Special Price', validators=[NumberRange(min=0)], render_kw={"type" : "number"}, default=0)
    special_datestart = DateField("Special Date Start", format="%Y-%m-%d", default=mindate, render_kw={"min" : mindate })
    special_dateend = DateField("Special Date End", format="%Y-%m-%d", default=date.today()+ timedelta(days=3), render_kw={"min" : mindate + timedelta(days=1)})


getProductMiniData = '''
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
'''

#########################################
################ ROUTES #################
#########################################
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
        sql = text(getProductMiniData)
        result = db.session.execute(sql)
        results = result.mappings().all()
        
        products = []
        for row in results:
            products.append(setProductJSON(row))

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
        
        product_id = AddNewProduct(form)

        if product_id > 0:
            product = getProductJSON(product_id)

            return jsonify({ "status": "success", "message": "Product is added", "product": product }), 200
        
        return jsonify({ "status": "error", "message": "Somthing went wrong, Product could not be created", "reason": form.errors }), 500
    
    return render_template('productform.html', form=form)


#Update/Edit product value
@productmanager.route("/productfield/<int:productid>", methods=["GET", "PUT"])
def productEdit(productid):
    form = ProductForm() 
    mainImgPath = ""
    sql = text("""
                SELECT 
                    P.id, 
                    P.name, 
                    P.description,
                    P.code,
                    P.instock,
                    P.onspecial,
                    P.showonline,
                    
                    --product main image
                    IFNULL(M.id, 0) AS imgid,
                    IFNULL(MU.id, 0) AS imgusedid,
                    CASE 
                        WHEN M.id IS NOT NULL THEN
                            '/static/images/'|| M.name ||'/thumb'|| M.ext
                        ELSE ''
                    END AS imgpath,
                    
                    --product normal prices
                    IFNULL(PP1.id, 0) AS normalpriceid,
                    IFNULL(PP1.price, 0.00) as normalprice,
               
                    --product special prices
                    IFNULL(PP2.id, 0) AS specialpriceid,
                    IFNULL(PP2.price, 0.00) as specialprice,
                    PP2.specialdateStart,
                    PP2.specialdateEnd

                FROM products AS P
                LEFT JOIN mediaused MU ON MU.id = P.mediaused_id AND MU.deleted_yn=0
                LEFT JOIN medias M ON M.id = MU.media_id AND M.deleted_yn=0
                LEFT JOIN productprice PP1 ON PP1.product_id = P.id AND PP1.isspecial=0 AND PP1.deleted_yn = 0
                LEFT JOIN productprice PP2 ON PP2.product_id = P.id AND PP2.isspecial=1 AND PP2.deleted_yn = 0
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

        form.main_mediaid.data = results["imgid"]
        mainImgPath = results["imgpath"]

        form.product_stock.data = results["instock"]
        form.product_special.data = results["onspecial"] == 1
        form.product_show.data = results["showonline"] == 1  
        
        form.price_normal.data = results["normalprice"]
        
        if results["onspecial"] == 1:
            form.price_special.data = results["specialprice"]
            form.special_datestart.data = results["specialdateStart"]
            form.special_dateend.data = results["specialdateEnd"]
            
    if request.method == 'PUT':
        if not form.validate_on_submit():
            return jsonify({ "status": "error", "message": "Product could not be updated", "reason": form.errors }), 500
    
        UpdateProduct(form, results["imgid"], results["imgusedid"], results["normalprice"], results["specialprice"])

        product = getProductJSON(productid)          
        
        return jsonify({ "status": "success", "message": "product is updated", "product": product }), 200
        
    return render_template('productform.html', form=form, mainImgPath=mainImgPath)


#########################################
############### Functions ###############
#########################################

def getProductJSON(productid):
    sql = text(getProductMiniData + " AND P.id=:productid")
    result = db.session.execute(sql, {"productid": productid})
    row = result.mappings().fetchone()     
    product = setProductJSON(row) 
    
    return product


def setProductJSON(row):
    return {
                "id": row["id"],
                "name": row["name"],
                "onspecial": row["onspecial"],
                "showonline": row["showonline"],
                "image": {
                    "path": row["path"]
                }
            }

########### ADD NEW PRODUCT DATA ###########
#Add New Product Image
def AddImg(form):
    sqlimg = text('''
                INSERT INTO mediaused ([media_id], [order], [function_as], [create_at], [deleted_yn])
                VALUES (:imgid, 0, "main product image", CURRENT_TIMESTAMP, 0)
                RETURNING id;
            ''')

    result = db.session.execute(sqlimg, {"imgid": form.main_mediaid.data})
    row_mediaused = result.fetchone()
    db.session.commit()

    return row_mediaused.id

#Add New Product Prices
def AddNewPrice(productid, form):
    sqlnewprice1 =text('''
        INSERT INTO productprice ([product_id], [price], [isspecial], [create_at], [deleted_yn])
        VALUES(:productid, :price, 0, CURRENT_TIMESTAMP, 0)
    ''')
    db.session.execute(sqlnewprice1, {"productid": productid, "price": form.price_normal.data, })        
    db.session.commit()

#Add New Product Special Prices
def AddNewSpecialPrice(productid, form):
    if form.product_special.data:
        sqlnewprice1 =text('''
            INSERT INTO productprice ([product_id], [price], [isspecial], [specialdataStart], [specialdataEnd], [create_at], [deleted_yn])
            VALUES(:productid, :price, 1, :datestart, :dateend, CURRENT_TIMESTAMP, 0)
        ''')
        db.session.execute(sqlnewprice1, {"productid": productid, "price": form.price_normal.data, "datestart":form.special_datestart.data, "dateend":form.special_dateend.data })        
        db.session.commit()

#Add New Product
def AddNewProduct(form):
    mediausedId = AddImg(form)

    sqlproduct = text('''
                        INSERT INTO products([mediaused_id], [name], [instock], [description], [code], [onspecial], [showonline], [create_at], [deleted_yn])
                        VALUES (:imgusedid, :name, :instock, :descript, :code, :onspecial, :showonline, CURRENT_TIMESTAMP, 0)
                          RETURNING id;
                    ''')

    result = db.session.execute(sqlproduct, 
                                {
                                    "imgusedid": mediausedId, 
                                    "name": form.product_name.data,
                                    "descript": form.product_decription.data,
                                    "code": form.product_code.data,  
                                    "instock": form.product_stock.data,
                                    "onspecial": 1 if form.product_special.data else 0,
                                    "showonline": 1 if form.product_show.data else 0
                                }
                                )
    row_product = result.fetchone()
    db.session.commit()   

    if row_product[0] > 0:
        AddNewPrice(row_product[0], form)  
        AddNewSpecialPrice(row_product[0], form) 
        
        return row_product[0]
    else:
        return 0       


########### UPDATE PRODUCT DATA ###########
# Update Existing Product Image
def ReplaceExistingImg(productid, newimgid, oldimgid, oldimgusedid):
    usedimgid = oldimgusedid
    
    if newimgid != oldimgid:
            sqlnewimg =text('''
                INSERT INTO mediaused ([media_id], [order], [function_as], [create_at], [deleted_yn])
                SELECT :imgid, 0, 'main product image', CURRENT_TIMESTAMP, 0
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM products AS P
                    LEFT JOIN mediaused MU ON MU.id = P.mediaused_id AND MU.deleted_yn=0
                    LEFT JOIN medias M ON M.id = MU.media_id AND M.deleted_yn=0
                    WHERE P.deleted_yn = 0 AND P.id=:productid AND IFNULL(M.id, 0)=:imgid
                )
                RETURNING id;
            ''')
            results = db.session.execute(sqlnewimg, {"productid": productid, "imgid": newimgid})
            row = results.fetchone()
            
            usedimgid = row[0]
            db.session.commit()       
    
    return usedimgid

#Update Existsing Product Prices
def ReplaceExistingPrice(productid, form, curnormprice):
    if form.price_normal.data != curnormprice:
        sqlnewprice1 =text('''
                INSERT INTO productprice ([product_id], [price], [isspecial], [create_at], [deleted_yn])
                SELECT :productid, :price, 0, CURRENT_TIMESTAMP, 0
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM products AS P
                    LEFT JOIN productprice PP1 ON PP1.product_id = P.id AND PP1.isspecial=0 AND PP1.deleted_yn = 0
                    WHERE P.deleted_yn = 0 AND P.id=:productid AND IFNULL(PP1.price, 0)=:price
                )
                RETURNING id;
            ''')
        results = db.session.execute(sqlnewprice1, {"productid": productid, "price": form.price_normal.data, })
        row = results.fetchone()
        
        db.session.commit()  

        sql =text('''
                UPDATE productprice SET [deleted_yn] = 1, [deleted_at]=CURRENT_TIMESTAMP
                WHERE product_id = :productid AND isspecial=0 AND deleted_yn = 0 AND id!=:id
            ''')
        db.session.execute(sql, {"productid": productid, "price": form.price_normal.data, "id": row[0] })
        db.session.commit()  

#Update Existsing Product Special Prices
def ReplaceExistingSpecialPrice(productid, form, curspecialprice):
    if form.product_special.data:

        if form.price_special.data != curspecialprice:
            sqlnewprice1 =text('''
                    INSERT INTO productprice ([product_id], [price], [isspecial], [specialdataStart], [specialdataEnd] [create_at], [deleted_yn])
                    SELECT :productid, :price, 1, :datestart, dateend CURRENT_TIMESTAMP, 0
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM products AS P
                        LEFT JOIN productprice PP1 ON PP1.product_id = P.id AND PP1.isspecial=1 AND PP1.deleted_yn = 0
                        WHERE P.deleted_yn = 0 AND P.id=:productid AND IFNULL(PP1.price, 0)=:price
                    )
                    RETURNING id;
                ''')
            results = db.session.execute(sqlnewprice1, {"productid": productid, "price": form.price_special.data, "datestart": form.special_datestart, "dateend": form.special_dateend})
            row = results.fetchone()
            
            db.session.commit()  

            sql =text('''
                    UPDATE productprice SET [deleted_yn] = 1, [deleted_at]=CURRENT_TIMESTAMP
                    WHERE product_id = :productid AND isspecial=1 AND deleted_yn = 0 AND id!=:id
                ''')
            db.session.execute(sql, {"productid": productid, "price": form.price_normal.data, "id": row[0] })
            db.session.commit()  

    else:
        sql =text('''
                    UPDATE productprice SET [deleted_yn] = 1, [deleted_at]=CURRENT_TIMESTAMP
                    WHERE product_id=:productid AND isspecial=1 AND deleted_yn = 0
                ''')
        db.session.execute(sql, {"productid": productid, "price": form.price_normal.data })
        db.session.commit()


# Update Existing Product
def UpdateProduct(form, curimgid, curimgusedid, curnormprice, curspecialprice):

    usedimgid = ReplaceExistingImg(form.product_id.data, form.main_mediaid.data, curimgid, curimgusedid)
    ReplaceExistingPrice(form.product_id.data, form, curnormprice)
    ReplaceExistingSpecialPrice(form.product_id.data, form, curspecialprice)

    found = False
    
    sqlproduct = text('''
                UPDATE products SET [name]=:name, [instock]=:instock, [description]=:descript, [code]=:code, 
                    [onspecial]=:onspecial, [showonline]=:showonline, [mediaused_id]=:mediausedid
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
                                        "mediausedid": usedimgid
                                    }
                                    )
    row_product = result.fetchone()
    db.session.commit()

    if usedimgid != curimgusedid:
        sqlusedimg =text('''
                UPDATE mediaused SET  [deleted_yn] = 1, [deleted_at]=CURRENT_TIMESTAMP
                WHERE id=:id
            ''')
        db.session.execute(sqlusedimg, {"id": curimgusedid})
        db.session.commit()

    if(row_product):
        found = True

    return found