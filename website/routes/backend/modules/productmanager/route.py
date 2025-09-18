from flask import jsonify, render_template, request
from . import productmanager, ProductForm

products = [
  {
    "id": 1, "name": "Product One", "image": { "id": 1, "path": "/static/images/img1/thumbs.png"},
  },
  {
    "id": 2, "name": "Product Two", "image": { "id": 2, "path": "/static/images/img2/thumbs.jpg",},
  },
]

#route
@productmanager.route('/', methods=["GET"])
def index():
    return  render_template("productmanager.html")


@productmanager.route('/getproducts', methods=["GET"])
def getproducts():
    if request.method == "GET":
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