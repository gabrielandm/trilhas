import urllib
import requests
from datetime import datetime
from sqlalchemy import Column, create_engine, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

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
    
    @property
    def serialize(self):
        return {
       	    'req_id': self.req_id,
            'req_date': self.req_date,
            'user_name': self.user_name,
            'repo_name' : self.repo_name
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

app = Flask(__name__)

# CREATE - NEW repositories
@app.route("/add-new/<string:user_name>")
def createNewRepo(user_name):
    return addNewRepo(user_name)

# READ - List ALL repositories
@app.route("/read-all")
def readAllRepos():
    return getAllRepos()

# READ - List repositories based on USERNAME
@app.route("/read-only/<string:user_name>")
def readReposByUsername(user_name):
    return getReposByUser(user_name)

def getAllRepos():
    repos = session.query(Repo).all()
    return jsonify(Repo=[repo.serialize for repo in repos])

def getReposByUser(user_name: str):
    repos = session.query(Repo).filter(Repo.user_name == user_name)
    return jsonify(Repo=[repo.serialize for repo in repos])

def addNewRepo(user_name: str):
    added = 0

    url = "https://api.github.com/users/" + user_name + "/repos"
    repos = requests.get(url)
    repos = repos.json()
    for repo in repos:
        added += 1
        create_repo = Repo(user_name = user_name, repo_name = repo["name"])
        session.add(create_repo)
        session.commit()
    
    return {
        'success': True,
        'added': added,
        'username_typed': user_name
    }


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)