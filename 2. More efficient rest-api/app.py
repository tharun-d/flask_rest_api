#pip install flask,flask-restful,flask-jwt

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = "HGJKGKHGYFVkljlh"

jwt = JWT(app, authenticate, identity) #localhost/auth post method
# Authorization for JWT
#so get method for Item requires authorization in headers with value JWT Token
#for this localhost/auth post method with body username and passsword in body if success then it returns token

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
            # only detect price and update even though there is another fields
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This cannot be blank or string"
        )
    @jwt_required() #requires authorization of jwt
    def get(self, name):
        item = next(filter(lambda x:x["name"] == name ,items),None) # next returns first item returned by filter if there is nothing it retrns none as we mentioned none
        return {"message":item}, 200 if item else 404
    
    def post(self, name):
        if next(filter(lambda x:x["name"] == name ,items),None):
            return { "message":f"item with {name} already exist" }, 400
        request_data = Item.parser.parse_args()
        item = {
            "name":name,
            "price":request_data["price"]
        }
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items # the items variable in this block is global one not new one
        items = list(filter(lambda x:x["name"] != name ,items))
        return {"message":"deleted"}

    def put(self, name):
       
        request_data = Item.parser.parse_args()
        item = next(filter(lambda x:x["name"] == name ,items),None)
        if item is None:
            item = {"name":name, "price":request_data["price"]}
            items.append(item)
        else:
            item.update(request_data)
        return item

class ItemList(Resource):
    def get(self):
        return {"items":items}

api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")

app.run(port = 5000, debug = True)

#200 success get
#201 success post
#400 Bad request already found you cant insert
#404 not found

