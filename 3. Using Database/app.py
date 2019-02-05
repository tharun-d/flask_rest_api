#pip install flask,flask-restful,flask-jwt

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from item import Item, ItemList
from user import UserRegister

app = Flask(__name__)
api = Api(app)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "HGJKGKHGYFVkljlh"

jwt = JWT(app, authenticate, identity) #localhost/auth post method
# Authorization for JWT
#so get method for Item requires authorization in headers with value JWT Token
#for this localhost/auth post method with body username and passsword in body if success then it returns token

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__": #below code only run only if you run python app.py
    app.run(port = 5000, debug = True)

#200 success get
#201 success post
#400 Bad request already found you cant insert
#404 not found
#500 internal server error like connection is open again you are trying to open

