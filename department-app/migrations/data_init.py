"""Module providing MySQL functions"""
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
            "CONSTRAINT PK_Category PRIMARY KEY (category_id));")
mydb.commit()


cursor.execute("CREATE TABLE Items ("
            "item_id INT(11) AUTO_INCREMENT,"
            "item_category_id INT(11) NOT NULL,"
            "item_label VARCHAR(100) NOT NULL,"
            "item_info TEXT,"
            "item_video_link VARCHAR(255),"
            "item_photo_link VARCHAR(255),"
            "CONSTRAINT PK_Item PRIMARY KEY(item_id),"
            "FOREIGN KEY (item_category_id) REFERENCES Categories(category_id)"
            "ON UPDATE CASCADE ON DELETE CASCADE);")
mydb.commit()


cursor.execute("INSERT INTO Categories (label) VALUES"
            "('Movies'),"
            "('Books'),"
            "('Details'),"
            "('TESTTT'),"
            "('DetaTERERERils'),"
            "('DetFDFDFDFDDails');")
mydb.commit()
cursor.execute(
"INSERT INTO Items (item_category_id,item_label,item_info,item_video_link,item_photo_link) VALUES"

"(1,'TESSSS','Lorem ipsum dolor sit amet, consectetur adipiscing elit','https://www.youtube.com/"
"embed/Zi_XLOBDo_Y','https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Michael_Jackson_Da"
"ngerous_World_Tour_1993.jpg/1200px-Michael_Jackson_Dangerous_World_Tour_1993.jpg'),"

"(1,'23523','Lorem ipsum dolor sit amet, consectetur adipiscing elit','https://www.youtube.com/"
"embed/dQw4w9WgXcQ','https://images.unsplash.com/photo-1554080353-a576cf803bda?ixlib=rb-4.0.3&"
"ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8cGhvdG98ZW58MHx8MHx8&w=1000&q=80'),"

"(3,'DFSDFS','Lorem ipsum dolor sit amet, consectetur adipiscing elit','https://www.youtube.com/"
"embed/4D7u5KF7SP8','https://media.istockphoto.com/id/912592258/photo/dog-surfing-on-a-wave.jpg?"
"s=612x612&w=0&k=20&c=ZGDzFIsXr4-kW7YoEo2blwiM5yqlSU0yOzYgXRRETgQ='),"

"(4,'dfvsfwe','Lorem ipsum dolor sit amet, consectetur adipiscing elit','https://www.youtube.com/"
"embed/HzdD8kbDzZA','https://media.gettyimages.com/id/1181462163/photo/happy-asian-toddler-girl"
"-with-sunglasses-smiling-joyfully-and-enjoying-family-bonding-time.jpg?s=612x612&w=gi&k=20&c="
"pc2ziPDglQ2FPcV7aEoSWbmSM-bwDwJTPCIFWwItYMQ='),"

"(2,'trte','Lorem ipsum dolor sit amet, consectetur adipiscing elit','https://www.youtube.com/"
"embed/lyWqQ4KzlzQ','https://images.unsplash.com/photo-1501426026826-31c667bdf23d?ixlib=rb-4.0.3"
"&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8c3VtbWVyJTIwZnVufGVufDB8fDB8fA%3D%3D&w=1000&q=80'),"

"(4,'vfrfre','Lorem ipsum dolor sit amet, consectetur adipiscing elit','https://www.youtube.com/"
"embed/bBD8M3WFrAw','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROUhw_cdYbqRXG7HRQp-"
"7OwCBl_9SZANCKGA&usqp=CAU'),"

"(1,'HELLOOOOOO','Lorem ipsum dolor sit amet, consectetur adipiscing elit','https://www.youtube."
"com/embed/tgbNymZ7vqY','https://cdn.britannica.com/38/200938-050-E22981D1/Freddie-Mercury-Live"
"-Aid-Queen-Wembley-Stadium-July-13-1985.jpg');")
mydb.commit()
cursor.close()
