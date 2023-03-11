import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123321",
  database="multilib_db"
)

cursor = mydb.cursor()
cursor.execute("CREATE TABLE Items ("
            "item_id INT(11) AUTO_INCREMENT,"
            "item_category_id INT(11) NOT NULL,"
            "item_label VARCHAR(100) NOT NULL,"
            "item_info TEXT,"
            "item_video_link VARCHAR(255),"
            "item_photo_link VARCHAR(255),"
            "CONSTRAINT PK_Item PRIMARY KEY(item_id),"
            "FOREIGN KEY (item_category_id) REFERENCES Categories(category_id) ON UPDATE CASCADE ON DELETE CASCADE);")
mydb.commit()
cursor.close()
