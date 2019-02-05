import mysql.connector
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_user_name(cls, username):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "SELECT * FROM users WHERE username = %s "
        mycursor.execute(sql,(username, ))
        myresult = mycursor.fetchone()
        if myresult:
            user = cls(*myresult)
        else:
            user = None
            connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "SELECT * FROM users WHERE id = %s "
        mycursor.execute(sql,(_id, ))
        myresult = mycursor.fetchone()
        if myresult:
            user = cls(*myresult)
        else:
            user = None
            connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
            # only detect price and update even though there is another fields
    parser.add_argument('username',
            type = str,
            required = True,
            help = "username cannot be blank"
        )
    parser.add_argument('password',
            type = str,
            required = True,
            help = "password cannot be blank"
        )
    def post(self):
        request_data = UserRegister.parser.parse_args()

        if User.find_by_user_name(request_data["username"]):
            return {"message":"username already exists"}, 400

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Passw0rd@12",
            database="FlaskRestApi"
            )
        mycursor = connection.cursor()
        sql = "insert into users (username, loginpassword) values (%s, %s)"     
        mycursor.execute(sql,(request_data["username"], request_data["password"] ))
        connection.commit()
        connection.close()
        return {"message":"User successfully created"}, 201