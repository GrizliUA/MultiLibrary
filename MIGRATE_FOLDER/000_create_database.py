import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123321",
)

cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS multilib_db");
mydb.commit()
cursor.close()