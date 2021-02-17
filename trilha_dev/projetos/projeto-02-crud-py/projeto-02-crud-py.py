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
            'price': self.price
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
        description = request.args.get('description', '')
        price = request.args.get('price', '')
        # Calling function to add new product to DB
        return addNewProduct(name, description, price)

# READ - Filtered listing
@app.route('/product-search', methods= ['GET'])
def readProducts():
    # Filtered search set False (Default)
    filtered = False
    equal = True
    # Getting all possible filters
    if request.args.get('name', '') is not None:
        filtered = True
        name = request.args.get('name', '')
    else:
        name = '%{}%'
    
    if request.args.get('description', '') is not None:
        filtered = True
        description = request.args.get('description', '')
    else:
        description = '%{}%'
    
    if request.args.get('price', '') is not None:
        filtered = True
        price = request.args.get('price', '')
        if request.args.get('higher', '') == 'true':
            higher = True
        else:
            higher = False
        if request.args.get('equal', '') == 'false':
            equal = False
    else:
        price = 1000000

    # Calling function to search for products
    if filtered == True:
        return searchFilteredProducts(name, description, price, higher, equal)
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
            print("Invalid float.")
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
        print("Product already exists.")
        return {
            'status': 'product not created',
            'reason': 'product already registered'
        }
    # Verify name lenght
    if len(name) > 32:
        print("Name is too big.")
        return {
            'status': 'product not created',
            'reason': 'name bigger than 32 characters'
        }
    # Verify description lenght
    if len(description) > 64:
        print("Description is too big.")
        return {
            'status': 'product not created',
            'reason': 'description bigger than 64 characters'
        }
    # Verify price limit
    if price > 99999.99:
        print("Price is too high.")
        return {
            'status': 'product not created',
            'reason': 'price is too high'
        }
    # Add new product
    else:
        new_product = Product(name = name, description = description, price = price)
        session.add(new_product)
        session.commit()

        print("Product created.")
        return {
            'status': 'product created',
            'reason': ''
        }

def searchFilteredProducts(name: str, description: str, price: str, higher: bool, equal: bool):
    if equal == True:
        if higher == True:
            print('Filtering...\n'
                'Name like ' + name + '\n'
                'description like ' + description + '\n',
                'price >= ' + price
            )
            products = session.query(Product).filter(
                Product.name.like(name),
                Product.description.like(description),
                Product.price >= price
            )
        else:
            print('Filtering...\n'
                'Name like ' + name + '\n'
                'description like ' + description + '\n',
                'price <= ' + price
            )
            products = session.query(Product).filter(
                Product.name.like(name),
                Product.description.like(description),
                Product.price <= price
            )
    else:
        if higher == True:
            print('Filtering...\n'
                'Name like ' + name + '\n'
                'description like ' + description + '\n',
                'price > ' + price
            )
            products = session.query(Product).filter(
                Product.name.like(name),
                Product.description.like(description),
                Product.price > price
            )
        else:
            print('Filtering...\n'
                'Name like ' + name + '\n'
                'description like ' + description + '\n',
                'price < ' + price
            )
            products = session.query(Product).filter(
                Product.name.like(name),
                Product.description.like(description),
                Product.price < price
            )
    
    return jsonify(Product=[products.serialize for product in products])

def searchAllProducts():
    print("Listing all products...")
    products = session.query(Product).all()
    
    return jsonify(Product=[products.serialize for product in products])

def removeProductByName(name: str):
    if session.query(Product).filter(Product.name == name).first() is None:
        print("Product not found.")
        return {
            'status': 'product not found',
            'reason': 'entered incorrect name'
        }
    else:
        print("Product deleted.")
        session.query(Product).filter(Product.name == name).delete(synchronize_session=False)
        return {
            'status': 'product deleted',
            'reason': ''
        }

def modifyProductValue(value_name: str, name: str, new_value: str or float):
    if value_name == 'description':
        if session.query(Product).filter(Product.name == name).first() is not None and len(new_value) <= 64:
            print("Product description modified.")
            session.query(Product).filter(Product.name == name).update(description = new_value, synchronize_session=False)
            return {
                'status': 'product description modified',
                'reason': ''
            }
        elif len(new_value) > 64:
            print('Description too big.')
            return {
                'status': 'description too big',
                'reason': 'description must be smaller than 64 characters'
            }
        else:
            print('Product not found')
            return {
                'status': 'product not found',
                'reason': 'name not found in database'
            }
    elif value_name == 'price':
        if session.query(Product).filter(Product.name == name).first() is not None and new_value < 100000:
            print("Product price modified.")
            session.query(Product).filter(Product.name == name).update(price = new_value, synchronize_session=False)
            return {
                'status': 'product price modified',
                'reason': ''
            }
        elif new_value >= 100000:
            print('Price too high.')
            return {
                'status': 'price too high',
                'reason': 'price must be lower than 100000'
            }
        else:
            print('Product not found')
            return {
                'status': 'product not found',
                'reason': 'name not found in database'
            }


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)