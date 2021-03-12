import httplib2

print("Running test for projeto 02")
address = 'http://localhost:5000'

# Test the creating of a new product with method POST
def add_new_product(name: str, description: str, price: float):
    new_product = {
        'name': name,
        'description': description,
        'price': price
    }
    url = address + "/product-subscription?name=" + new_product['name'] + "&description=" + new_product['description'] +  "&price=" + new_product['price']
    h = httplib2.Http()
    result = h.request(url, 'POST')

print("Test 1 - Succesfull creation")
add_new_product("name", "description", "10.00")

print("Test 2 - Same name")
add_new_product("name", "description", "10.00")

print("Test 3 - Name is too big")
add_new_product("namenamenamenamenamenamenamenamenamename", "description", "10.00")

print("Test 4 - Description is too big")
add_new_product("eman", "descriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescript", "10.00")

print("Test 5 - Price is too big")
add_new_product("eman", "description", "100000.00")
