from . import *

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


def get_cart():
    return session.get('cart', {})

@cartpages.route("/")
def cart():
    cart = get_cart()

    productsArr = [pid for pid, qty in cart.items()]
    productIds = ",".join(productsArr)
    
    sql = text(f'{sqlproduct}AND P.id IN ({productIds})')
    result= db.session.execute(sql)
    products = [dict(row) for row in result.mappings()]

    for product in products:
        id = str(product["id"])
        qty = cart[id]
        product["qty"] = qty

    total = sum( [products["qty"] * products["normalprice"]  for products in  products] )
    
    return  render_template("cart.html", products=products, total=total)

@cartpages.route("/add/", methods=["POST"])
def cart_add():    
    
    if request.method == 'POST':
        productid = int(request.form.get('id',0))
        print(productid)
        if productid > 0:
            qty = int(request.form.get('qty',1))
            cart = get_cart()
            cart[str(productid)] = cart.get(str(productid), 0) + qty
            session['cart'] = cart
            return jsonify({ "status": "success", "message": "Product is Added"}), 200
        
        return jsonify({ "status": "error", "message": "product not found"}), 404
    return 


@cartpages.route("/remove/", methods=["POST"])
def cart_remove():    
    
    if request.method == 'POST':
        productid = int(request.form.get('id',0))
        if productid > 0:
            qty = int(request.form.get('quantity',1))
            cart = get_cart()
            num = cart.get(str(productid), 0) - qty
            
            if num > 0:
                cart[str(productid)] = num
            else:
                cart.pop(str(productid), None)
                
            session['cart'] = cart
            return jsonify({ "status": "success", "message": "Product is removed"}), 200
        
        return jsonify({ "status": "error", "message": "product not found"}), 404
    return 

@cartpages.route("/checkout")
def checkout():
    pass