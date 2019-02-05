#pip install flask,flask-restful,flask-jwt_extended

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from item import Item, ItemList
from user import UserRegister, UserLogin, UserDelete

app = Flask(__name__)
api = Api(app)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "HGJKGKHGYFVkljlh"

jwt = JWTManager(app) #will not create any post automatically
# Authorization for JWT
#so get method for Item requires authorization in headers with value Bearer accessToken

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    else:
        return {"is_admin": False}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserDelete, "/delete")

if __name__ == "__main__": #below code only run only if you run python app.py
    app.run(port = 5000, debug = True)

#200 success get
#201 success post
#400 Bad request already found you cant insert
#404 not found
#500 internal server error like connection is open again you are trying to open

