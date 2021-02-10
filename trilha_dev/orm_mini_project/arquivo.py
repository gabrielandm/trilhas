import urllib

from datetime import datetime

from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship # Not needed
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import sessionmaker

# TODO: Connect to Azure LATER
# params = urllib.parse.quote_plus(
#     'Driver=%s;' % driver +
#     'Server=tcp:%s,1433;' % server +
#     'Database=%s;' % database +
#     'Uid=%s;' % username +
#     'Pwd={%s};' % password +
#     'Encrypt=yes;' +
#     'TrustServerCertificate=no;' +
#     'Connection Timeout=30;')

# conn_str = 'mssql+pyodbc:///?odbc_connect=' + params
# engine = create_engine(conn_str)

Model = declarative_base(name='Model')

class Repo(Model):
    __tablename__ = "repo"

    req_id = Column(Integer, primary_key=True, autoincrement=True)
    req_date = Column(DateTime, nullable=False, default=datetime.now())
    user_name = Column(String(30), nullable=False)
    repo_name = Column(String(30), nullable=False)

    def __init__(self, user_name, repo_name):
         self.user_name = user_name
         self.repo_name = repo_name

def run(rep_name: str, rep_user: str):

    driver = "{ODBC Driver 17 for SQL Server}"
    server = "kumulus-paoli.database.windows.net"
    database = "test_database"
    user = "login"
    password = "Password123"

    conn = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+user+';PWD='+password

    params = urllib.parse.quote_plus(conn)
    conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)
    engine = create_engine(conn_str, echo=False)
    Model.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # create a fake repo
    create_repo = Repo(user_name=rep_user, repo_name=rep_name)
    print(datetime.now())
    session.add(create_repo)
    session.commit()

    select = session.query(Repo).all()
    print(select[0].repo_name)

run("fake_user_name", "fake_repo_name")
