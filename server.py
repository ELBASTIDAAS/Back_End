import random
from flask import Flask, request, abort
import json
from config import me
from mock_data import catalog
from config import db
from bson import ObjectId

app = Flask("server")


@app.get("/")
def home():
    return "Hello world!"


@app.get("/test")
def test():
    return "This is another endpoint"


@app.get("/about")
def about():
    return "Miguel Bastidas"


###########################################
############## CATALOG API ################
###########################################

@app.get("/api/version")
def version():
    version = {
        "v": "v1.0.4",
        "name": "zombie rabbit",
    }
    # parse a direct into json string
    return json.dumps(version)

#get /api/about
# return me as jsno


@app.get("/api/about")
def api_about():
    return json.dumps(me)

# return catalog


@app.get("/api/catalog")
def get_catalog():
    # read from db
    cursor = db.Products.find({})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

# POST /api/catalog


@app.post("/api/catalog")
def save_catalog():
    product = request.get_json()
    # validation
    if "title" not in product:
        return {"error": "title is required"}, 400

    # the title shopuld have at least 5 chars
    if len(product["title"]) < 4:
        return {"error": "title should be at least 4 chars"}, 400

    # there must have a category
    if "category" not in product:
        return {"error": "category is required"}, 400

    # must have a price
    if "price" not in product:
        return {"error": "price is required"}, 400

    # price must be a number
    if not isinstance(product["price"], (int, float)):
        return {"error": "price must be a number"}, 400

    # the price should be greater than 0
    if product["price"] < 0:
        return {"error": "price should be greater than 0"}, 400

    # assign a unique _id to product
    product["_id"] = random.randint(1000, 10000)

    # add product to catalog
    db.Products.insert_one(product)
    product["_id"] = str(product["_id"])

    catalog.append(product)
    return json.dumps(product)


# return the number of products in the list
@app.get("/api/test/count")
def test_count():
    return len(catalog)


@app.get("/api/catalog/<category>")
def by_category(category):
    # filter the catalog by category
    # return the filtered list
    results = []
    category = category.lower()
    for product in catalog:
        if product["category"].lower() == category:
            results.append(product)
    return category


@app.get("/api/catalog/search/<text>")
def search(text):
    # filter the catalog by category
    # return the filtered list
    results = []
    text = text.lower()
    for product in catalog:
        if text in product["title"].lower() or text in product["category"].lower():
            results.append(product)
    return json.dumps(results)

#GET /api/categories


@app.get("/api/categories")
def get_categories():
    results = []
    for product in catalog:
        cat = product["category"]
        if not cat in results:
            results.append(cat)
    return json.dumps(results)


#get /api/test/value
# sum all prices and return the results
@app.get("/api/test/value")
def test_value():
    total = 0
    for product in catalog:
        total = total + product["price"]
    return json.dump(total)

# create an endpoint that return the cheapest product


@app.get("/api/cheapest")
def get_cheapest():
    cheapest = catalog[0]
    for product in catalog:
        if product["price"] < cheapest["price"]:
            cheapest = product
    return json.dumps(cheapest)


# create anm endpoint that return a product based on give _id
@app.get("/api/product/<id>")
def get_product(id):
    for product in catalog:
        if product["_id"] == id:
            return json.dumps(product)
    return "Not found", 404


app.run(debug=True)


ages = [12, 34, 15, 73, 73, 13, 97, 23, 95,
        23, 98, 53, 83, 45, 90, 23, 75, 23, 78]
