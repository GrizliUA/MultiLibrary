import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123321",
  database="multilib_db"
)

cursor = mydb.cursor()
cursor.execute("CREATE TABLE Categories("
            "category_id INT(11) AUTO_INCREMENT,"
            "label VARCHAR(100) NOT NULL,"
            "CONSTRAINT PK_Category PRIMARY KEY (category_id));");
mydb.commit()
cursor.close()
