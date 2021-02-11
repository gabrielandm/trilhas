import requests # requests package to make the request and transform JSON into a DICT 
import textwrap
import pyodbc

# Specify driver
driver = '{ODBC Driver 17 for SQL Server}'

# Specify the Server name and the Database name
server_name = 'kumulus-paoli.database.windows.net'
database_name = 'test_database'
# Server URL
server = 'kumulus-paoli.database.windows.net,1433'
# Username and Password
username = 'login'
password = 'Password123'

# Full conection string
connection_string = textwrap.dedent('''
    Driver={driver};
    Server={server};
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=45;
'''.format(
    driver = driver,
    server = server,
    database = database_name,
    username = username,
    password = password
))

# Create a new PYODBC Connection Object
connection: pyodbc.Connection = pyodbc.connect(connection_string)

# Create a new Cursor Object
cursor: pyodbc.Cursor = connection.cursor()

select = 'select * from dbo.repo;'

def save_rep_names_sql(username): # Define the function used to list all repos names, and use the username as a parameter
    url = "https://api.github.com/users/" + username + "/repos" # Save the URL using the username received
    repos = requests.get(url) # Save the content of the request made to the URL 
    repos = repos.json() # Save only the JSON content into the repos variable (transforms into a dict type)

    for repo in repos: # For each dict inside the repos, create a dict called repo with the contents inside
        insert = "insert into dbo.repo (user_name, repo_name) values ('" + username + "', '" + repo["name"] + "');"
        cursor.execute(insert)
        cursor.commit()

# Call the function to see if it works:


# Close the connection
connection.close()