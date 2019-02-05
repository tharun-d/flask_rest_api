from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

import mysql.connector

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
        item = Item.find_by_name(name)
        if item:
            return item
        else:
            return {"message": "item not found"} ,404
            
    @classmethod
    def find_by_name(cls, name):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "SELECT * FROM items WHERE itemname = %s "
        mycursor.execute(sql,(name, ))
        item_present = mycursor.fetchone()
        connection.close()
        if item_present:
            return {"item":{"name":item_present[0], "price": item_present[1]}}

    def post(self, name):
        if Item.find_by_name(name):
            return { "message":f"item with {name} already exist" }, 400
        request_data = Item.parser.parse_args()
        item = {"name":name, "price":request_data["price"]}
        try:
            Item.insert(item)
        except:
            return {"message": "an error occured while inserting new item"}, 500

        return item, 201
    
    @classmethod
    def insert(cls, item):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "insert into items values(%s, %s)"
        mycursor.execute(sql,(item["name"], item["price"]))
        item = {
            "name": item["name"],
            "price": item["price"]
        }
        connection.commit()
        connection.close()
        return item
    
    def delete(self, name):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "delete from items where itemname = %s"
        mycursor.execute(sql,(name,))
        connection.commit()
        connection.close()
        return {"message":"deleted"}

    def put(self, name):  
        request_data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {"name": name, "price":request_data["price"]}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "an error occured while inserting new item"}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "an error occured while updating item"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "update items set price =%s where itemname = %s"
        mycursor.execute(sql,(item["price"],item["name"]))
        connection.commit()
        connection.close()
        return item

class ItemList(Resource):
    def get(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "SELECT * FROM items"
        mycursor.execute(sql)
        items_present = mycursor.fetchall()
        items = []
        for row in items_present:
            items.append({"name": row[0], "price": row[1]})
        connection.close()
        return {"items":items}
