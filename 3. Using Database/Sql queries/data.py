# connecting
import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Passw0rd@12",
  database="FlaskRestApi"
)

mycursor = connection.cursor()
sql = "SELECT * FROM users WHERE username = %s "
mycursor.execute(sql,('bob', ))
myresult = mycursor.fetchone()
connection.close()
print(myresult[0])