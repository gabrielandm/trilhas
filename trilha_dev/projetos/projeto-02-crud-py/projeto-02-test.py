import httplib2

address = 'http://localhost:5000'

# Test the creating of a new product with method POST
def add_new_product(name: str, description: str, price: str):
    new_product = {
        'name': name,
        'description': description,
        'price': price
    }
    url = address + "/product-subscription?name=" + new_product['name'] + "&description=" + new_product['description'] +  "&price=" + new_product['price']
    h = httplib2.Http()
    result = h.request(url, 'POST')

def delete_product(name: str):
    url = address + "/product-deletion?name=" + name
    h = httplib2.Http()
    result = h.request(url, 'DELETE')

def update_product(value_name: str, name: str, new_value: str):
    url = address + "/product-update?value_name=" + value_name + "&name=" + name + "&new_value=" + new_value
    h = httplib2.Http()
    result = h.request(url, 'PUT')

def search_filtered_product_name(name: str):
    url = address + "/product-search?name=" + name
    h = httplib2.Http()
    result = h.request(url, 'GET')

def test_add_new_product():
    print("\n\nRunning creation test for Projeto 02")

    print("Test 1 - Succesfull creation")
    add_new_product("name", "description", "10.00")

    print("Test 2 - Same name")
    add_new_product("name", "description", "10.00")
    delete_product("name")

    print("Test 3 - Name is too big")
    add_new_product("namenamenamenamenamenamenamenamenamename", "description", "10.00")

    print("Test 4 - Description is too big")
    add_new_product("eman", "descriptiondescriptiondescriptiondescriptiondescriptiondescriptiondescript", "10.00")

    print("Test 5 - Price is too big")
    add_new_product("eman", "description", "100000.00")

def test_delete_product():
    print("\n\nRunning deletion test for Projeto 02")

    print("Test 1 - Succesfull delete")
    add_new_product("product+to+delete", "", "100")
    delete_product("product+to+delete")

def test_update_product():
    print("\n\nRunning update test for Projeto 02")

    print("Test 1 - Succesfull update")
    add_new_product("product+to+update", "", "100")
    update_product("description", "product+to+update", "Updated description")
    search_filtered_product_name("product+to+update")
    #delete_product("product+to+update")

# test_add_new_product()
# test_delete_product()
test_update_product()