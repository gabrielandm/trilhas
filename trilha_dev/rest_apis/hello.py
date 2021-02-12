from flask import Flask
app = Flask('rest_apis')

@app.route('/')
def hello_world():
    return 'Hello, World!'