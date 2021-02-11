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

def run():

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

    # # create a fake repo
    # create_repo = Repo(user_name="fake_user", repo_name="fake_repo")
    # print(datetime.now())
    # session.add(create_repo)
    # session.commit()

    # query the repos - III
    for repo_select in session.query(Repo).all():
        print(repo_select.repo_name)

run()
