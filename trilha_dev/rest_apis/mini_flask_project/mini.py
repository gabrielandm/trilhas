from flask import Flask
app = Flask(__name__) 

@app.route("/puppies")
def puppiesFunction():
  return "Yes, puppies!"
  
@app.route("/puppies/<int:id>") # This is how you can GET a parameter from URL
def puppiesFunctionId(id):
  return "This method will act on the puppy with id %s" % id

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
