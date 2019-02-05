from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        "name":"My store",
        "items":[
            {
                "name":"My item",
                "price":10
            }
        ]
    }
]


@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items":[]
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>', methods = ['GET'])
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
        else :
            return jsonify({"message":"not found"})

@app.route('/store', methods = ['GET'])
def get_stores():
   return jsonify({"store":stores})

@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    print(name)
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name":request_data["name"],
                "price":request_data["price"]
            }
            store["items"].append(new_item)
            return jsonify(new_item)
        else :
            return jsonify({"message":"not found"})

@app.route('/store/<string:name>/item', methods = ['GET'])
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items":store["items"]})
        else :
            return jsonify({"message":"not found"})

app.run(port = 5000)
