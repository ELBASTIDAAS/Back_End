from flask import Flask
import json
from config import me

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
#return me as jsno

@app.get("/api/about")
def api_about():
    return json.dumps(me)



app.run(debug=True)