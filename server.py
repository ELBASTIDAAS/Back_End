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


@app.post("/api/catalog")
def save_product():
    if "title" not in product:
        abort(400, "Title is required")
    if len(product["title"]) < 5:
        abort(400, "Title is too short")
    if "category" not in product:
        abort(400, "Category is required")
    if "price" not in product:
        abort(400, "Price is required")
    if not isinstance(product["price"], float, int):
        abort(400, "Price must be a number")
    if product["price"] < 0:
        abort(400, "Price must be grater than 0")

    db.Products.insert_one(product)
    product["_id"] = str(product["_id"])
    return json.dumps(product)


@app.get("/api/test/count")
def num_of_prdoducts():
    return len(catalog)


@app.get("/api/about")
def api_about():
    return json.dumps(me)


app.run(debug=True)
