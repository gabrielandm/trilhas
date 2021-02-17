import urllib
from sqlalchemy import Float, String, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from flask import Flask, request

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
        print("Value is too big.")
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
    
if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)