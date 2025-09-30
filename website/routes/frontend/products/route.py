from website.app import db
from sqlalchemy import text
import os

from flask import Blueprint, redirect, render_template, url_for
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
Static_FOLDER = os.path.join(os.path.dirname(__file__), "static")
print(BASE_DIR)

productpages = Blueprint('productpages', __name__, template_folder="templates", static_folder='static', url_prefix='/products')


sqlproduct = '''
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
            '/static/images/'|| M.name ||'/medium'|| M.ext
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
WHERE P.deleted_yn = 0 AND P.showonline = 1
'''


@productpages.route('/')
def products():
    sql = text(sqlproduct)
    result = db.session.execute(sql)
    products = result.mappings().all()

    return  render_template("products.html", products=products)

@productpages.route('/<int:product_id>')
def product(product_id):
    sql = text(sqlproduct+" AND P.id=:productid")
    result= db.session.execute(sql, {"productid": product_id})
    product = result.mappings().fetchone()
    
    if product:
        return  render_template("product.html", product=product)
    

    return render_template('404.html'), 404