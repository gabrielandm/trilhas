import urllib
import requests

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
from sqlalchemy.orm import Session

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

def save_repos(session: Session, username: str): # Use the session and the username name as Str
    url = "https://api.github.com/users/" + username + "/repos"
    repos = requests.get(url)
    repos = repos.json()

    for repo in repos:
        create_repo = Repo(user_name = username, repo_name = repo["name"])
        session.add(create_repo)
        session.commit()

def print_all_repos_sql(session: Session): # Use the session
    for repo_select in session.query(Repo).all():
        print(repo_select.repo_name)

# Try the functions:
