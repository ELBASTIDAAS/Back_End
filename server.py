import random
from flask import Flask, request, abort
import json
from config import me
from mock_data import catalog
from config import db
from bson import ObjectId
from flask_cors import CORS

app = Flask("server")
CORS(app)  # enable CORS, for development only


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

# GET /api/catalog
# returns the catalog as json
# try it in the browser


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

    # save product on db
    db.Products.insert_one(product)
    product["_id"] = str(product["_id"])

    catalog.append(product)
    return json.dumps(product)


# return the number of products in the list
@app.get("/api/test/count")
def num_of_products():
    count = db.Products.count_documents({})
    return json.dumps({"total": count})


@app.get("/api/catalog/<category>")
def by_category(category):
    # filter the catalog by category
    # return the filtered list
    results = []
    cursor = db.Products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
    return json.dumps(results)


@app.get("/api/catalog/search/<text>")
def search(text):
    # filter the catalog by category
    # return the filtered list
    results = []
    text = text.lower()
    cursor = db.Products.find({"title": {"$regex": text, "$options": "i"}})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
    return json.dumps(results)

#GET /api/categories


@app.get("/api/categories")
def get_categories():
    results = []
    cursor = db.Products.distinct("category")
    for cat in cursor:
        results.append(cat)
    return json.dumps(results)


#get /api/test/value
# sum all prices and return the results
@app.get("/api/test/value")
def test_value():
    total = 0
    # get all the products from the DB
    # sum the price of each product
    # return the total
    cursor = db.Products.find({})
    for prod in cursor:
        total += prod["price"]
    return json.dump(total)

# create an endpoint that return the cheapest product


@app.get("/api/cheapest")
def get_cheapest():
    cursor = db.Products.find({})
    cheapest = cursor[0]
    for product in cursor:
        if product["price"] < cheapest["price"]:
            cheapest = product
    return json.dumps(cheapest)


# create anm endpoint that return a product based on give _id
@app.get("/api/product/<id>")
def get_product(id):
    objId = ObjectId(id)
    prod = db.Products.find_one({"_id": objId})
    if not prod:
        return abort(404, "Product not found")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)


# app.run(debug=True)


##############################################################################
###################### COUPON CODES ##########################################
##############################################################################

# save: POST /api/coupons
@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()
    # validation
    if "code" not in coupon:
        abort(400, "code is required")

    # the code shopuld have at least 5 chars
    # if len(coupon["code"]) < 4:
        # return {"error": "code should be at least 4 chars"}, 400

    # there must have a discount
    if "discount" not in coupon:
        abort(400, "Discount is required")

    # # must have a price
    # if "price" not in coupon:
    #     return {"error": "price is required"}, 400

    # # price must be a number
    # if not isinstance(coupon["price"], (int, float)):
    #     return {"error": "price must be a number"}, 400

    # # the price should be greater than 0
    # if coupon["price"] < 0:
    #     return {"error": "price should be greater than 0"}, 400

    # save product on db
    db.Coupons.insert_one(coupon)
    coupon["_id"] = str(coupon["_id"])

    return json.dumps(coupon)

# get: GET /api/coupons


@app.get("/api/coupons")
def get_coupons():
    cursor = db.Coupons.find({})
    results = []
    for coupon in cursor:
        coupon["_id"] = str(coupon["_id"])
        results.append(coupon)

    return json.dumps(results)

# get by id: GET /api/coupons/<id>


@app.get("/api/coupons/<id>")
def get_coupon(id):
    objId = ObjectId(id)
    coupon = db.Coupons.find_one({"_id": objId})
    if not coupon:
        return abort(404, "Coupon not found")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

# get by code GET /api/coupons/validate/<code>


@app.get("/api/coupons/validate/<code>")
def validate_coupon(code):
    coupon = db.Coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Invalid Code")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)
