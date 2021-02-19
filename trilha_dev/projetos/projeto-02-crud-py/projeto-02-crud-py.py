import urllib
from sqlalchemy import Float, String, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from flask import Flask, request, jsonify

app = Flask(__name__)
Model = declarative_base(name='Model')

class Product(Model):
    __tablename__ = "product"

    name = Column(String, primary_key=True)
    description = Column(String, nullable=False, default="No description")
    price = Column(Float(7,2), nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price
    
    @property
    def serialize(self):
        return {
       	    'name': self.name,
            'description': self.description,
            'price': float(self.price)
        }

driver = "{ODBC Driver 17 for SQL Server}"
server = "kumulus-paoli.database.windows.net"
database = "test_database"
user = "login"
password = "Password123"
conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""

params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)
engine = create_engine(conn_str, echo=False)
Model.metadata.create_all(engine)
session = Session(engine)

# CREATE - Add new products to the DB (products)
@app.route('/product-subscription', methods= ['POST'])
def createNewProduct():
    if request.method == 'POST':
        # Taking values from URL
        name = request.args.get('name', '')
        if name == '':
            return {
                "status": "Creation failed",
                "reason": "The product name entered is null"
            }
        description = request.args.get('description', '')
        price = request.args.get('price', '')
        # Calling function to add new product to DB
        return addNewProduct(name, description, price)

# READ - Filtered listing
@app.route('/product-search', methods= ['GET'])
def readProducts():
    # Filtered search set False (Default)
    filtered = False
    price_equal = True
    name_equal = False
    higher = False
    # Getting all possible filters
    if request.args.get('name', '') != '':
        filtered = True
        name = request.args.get('name', '')
        if request.args.get('name-equal', '') == 'true':
            name_equal = True
    else:
        name = ''
    
    if request.args.get('description', '') != '':
        filtered = True
        description = request.args.get('description', '')
    else:
        description = ''
    
    if request.args.get('price', '') != '':
        filtered = True
        price = request.args.get('price', '')
        if request.args.get('higher', '') == 'true':
            higher = True
        if request.args.get('price-equal', '') == 'false':
            price_equal = False
    else:
        price: float = 1000000

    try:
        price = float(price)
    except:
        return {
            'status': 'could not update product',
            'reason': 'invalid float entered'
        }

    # Calling function to search for products
    if filtered == True:
        return searchFilteredProducts(name, description, price, higher, price_equal, name_equal)
    else:
        return searchAllProducts()

# UPDATE - Update product description OR price
@app.route('/product-update', methods=['PUT'])
def updateProductByName():
    value_name = request.args.get('value_name', '')
    name = request.args.get('name', '')
    new_value = request.args.get('new_value', '')

    if value_name == 'price':
        try:
            new_value = float(new_value)
        except:
            return {
                'status': 'could not update product',
                'reason': 'invalid float entered'
            }

    return modifyProductValue(value_name, name, new_value)

# DELETE - Delete product by name
@app.route('/product-deletion', methods=['DELETE'])
def deleteProductByName():
    name = request.args.get('name', '')
    return removeProductByName(name)

def addNewProduct(name: str, description: str, price: str):
    name = name.upper()
    price = float(price)

    # Verify if product already exists
    if session.query(Product).filter(Product.name == name).first() is not None:
        return {
            'status': 'product not created',
            'reason': 'product already registered'
        }
    # Verify name lenght
    if len(name) > 32:
        return {
            'status': 'product not created',
            'reason': 'name bigger than 32 characters'
        }
    # Verify description lenght
    if len(description) > 64:
        return {
            'status': 'product not created',
            'reason': 'description bigger than 64 characters'
        }
    # Verify price limit
    if price > 99999.99:
        return {
            'status': 'product not created',
            'reason': 'price is too high'
        }
    # Add new product
    else:
        new_product = Product(name = name, description = description, price = price)
        session.add(new_product)
        session.commit()

        return {
            'status': 'product created',
            'reason': ''
        }

def searchFilteredProducts(name: str, description: str, price: float, higher: bool, price_equal: bool, name_equal: bool):
    if name_equal == False:
        if price_equal == True:
            if higher == True:
                products = session.query(Product).filter(
                    Product.name.like("%" + name + "%"),
                    Product.description.like("%" + description + "%"),
                    Product.price >= price
                )
            else:
                products = session.query(Product).filter(
                    Product.name.like("%" + name + "%"),
                    Product.description.like("%" + description + "%"),
                    Product.price <= price
                )
        else:
            if higher == True:
                products = session.query(Product).filter(
                    Product.name.like("%" + name + "%"),
                    Product.description.like("%" + description + "%"),
                    Product.price > price
                )
            else:
                products = session.query(Product).filter(
                    Product.name.like("%" + name + "%"),
                    Product.description.like("%" + description + "%"),
                    Product.price < price
                )
    else:
        if price_equal == True:
            if higher == True:
                products = session.query(Product).filter(
                    Product.name.like(name),
                    Product.description.like("%" + description + "%"),
                    Product.price >= price
                )
            else:
                products = session.query(Product).filter(
                    Product.name.like(name),
                    Product.description.like("%" + description + "%"),
                    Product.price <= price
                )
        else:
            if higher == True:
                products = session.query(Product).filter(
                    Product.name.like(name),
                    Product.description.like("%" + description + "%"),
                    Product.price > price
                )
            else:
                products = session.query(Product).filter(
                    Product.name.like(name),
                    Product.description.like("%" + description + "%"),
                    Product.price < price
                )
    return jsonify(products_json=[product.serialize for product in products])

def searchAllProducts():
    products = session.query(Product).all()
    return jsonify(products_json=[product.serialize for product in products])

def removeProductByName(name: str):
    if session.query(Product).filter(Product.name == name).first() is None:
        return {
            'status': 'product not found',
            'reason': 'entered incorrect name'
        }
    else:
        session.query(Product).filter(Product.name == name).delete(synchronize_session=False)
        return {
            'status': 'product deleted',
            'reason': ''
        }

def modifyProductValue(value_name: str, name: str, new_value: str or float):
    if value_name == 'description':
        if session.query(Product).filter(Product.name == name).first() is not None and len(new_value) <= 64:
            session.query(Product).filter(Product.name == name).update({"description": new_value}) #description = new_value, synchronize_session=False
            return {
                'status': 'product description modified',
                'reason': ''
            }
        elif len(new_value) > 64:
            return {
                'status': 'description too big',
                'reason': 'description must be smaller than 64 characters'
            }
        else:
            return {
                'status': 'product not found',
                'reason': 'name not found in database'
            }
    elif value_name == 'price':
        if session.query(Product).filter(Product.name == name).first() is not None and new_value < 100000:
            session.query(Product).filter(Product.name == name).update({"price": new_value}, synchronize_session=False)
            return {
                'status': 'product price modified',
                'reason': ''
            }
        elif new_value >= 100000:
            return {
                'status': 'price too high',
                'reason': 'price must be lower than 100000'
            }
        else:
            return {
                'status': 'product not found',
                'reason': 'name not found in database'
            }


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)