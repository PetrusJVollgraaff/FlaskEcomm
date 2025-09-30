from . import *

def get_cart():
    return session.get('cart', {})

@cartpages.route("/")
def cart():
    cart = get_cart()
    print(cart)
    items, toatal=[], 0.0

    for pid, qty in cart.items():
        pass
    pass

    return  render_template("cart.html")

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