from urllib import parse
from sqlalchemy import create_engine
import pyodbc

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



driver = "{ODBC Driver 17 for SQL Server}"
server = "kumulus-paoli.database.windows.net"
database = "test_database"
user = 'login'
password = 'Password123'

# connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:kumulus-paoli.database.windows.net,1433;Database=test_database;Uid=login;Pwd=Password123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
connection_string = '@kumulus-paoli.database.windows.net/test_database?driver=ODBC Driver 17 for SQL Server;Encrypt=yes;TrustServerCertificate=no;Uid=login;Pwd=Password123'
# params = parse.quote_plus(connection_string)

engine = create_engine("mssql+pyodbc://" + connection_string)
connection = engine.connect()
result = connection.execute("select 1+1 as res")
for row in result:
    print("res: ", row['res'])

connection.close()
