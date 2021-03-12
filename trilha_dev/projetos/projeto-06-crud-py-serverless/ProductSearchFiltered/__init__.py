import logging
import urllib
import json
from sqlalchemy import Float, String, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import azure.functions as func

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

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
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
    except:
        logging.info('Connection failed :(')
        pass
    
    try:
        name = req.params.get('name')
        exact = req.params.get('exact')

        if exact == "true":
            products = session.query(Product).filter(
                Product.name.like(name)
            )
        else:
            products = session.query(Product).filter(
                Product.name.like("%" + name + "%")
            )
        products_json = [product.serialize for product in products]
    except:
        logging.info('Query or Serialized failed')

    try:
        return func.HttpResponse(
            json.dumps(products_json)
        )
    except:
        logging.info('Return failed :(')
        pass

    return func.HttpResponse(":(")
