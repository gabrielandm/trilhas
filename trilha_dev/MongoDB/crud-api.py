from flask import Flask, jsonify, request, Response
from flask_mongoengine import MongoEngine
from mongoengine import Q
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {'host':'mongodb+srv://login:Password123@cluster0.iaj61.mongodb.net/Products'}
db = MongoEngine(app)

class Product(db.Document):
    name = db.StringField()
    description = db.StringField()
    price = db.FloatField()

# READ
@app.route('/products', methods=['GET'])
def readAllProducts():
    products = []

    for product in Product.objects:
        products.append(product)

    return jsonify(products)

@app.route('/products/<string:nm>', methods=['GET'])
def readProductsByName(nm):
    print(nm)
    products = []
    for product in Product.objects.filter(name=nm):
        products.append(product)

    return jsonify(products)

# CREATE
@app.route('/products', methods=['POST'])
def createProduct():
    data = request.json
    nm = data['name']
    desc = data['description']
    prc = data['price']

    protuct = Product(name = nm, description = desc, price = prc)
    protuct.save()

    return Response('{"created": true}', status = 201)

# UPDATE
@app.route('/products', methods=['PUT'])
def updateProduct():
    data = request.json
    nm = data['name']
    desc = data['description']
    prc = data['price']

    for product in Product.objects(name = nm):
        product.update(set__description=str(desc))
        product.update(set__price=float(prc))

    return Response('{"update": true}', status = 200)

#DELETE
@app.route('/products/<string:nm>', methods=['DELETE'])
def deleteProduct(nm):
    product = Product.objects.filter(name=nm).first()
    product.delete()

    return Response('{"deleted"=true}', 200)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3333)