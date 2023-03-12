"""Modules providing Flask realising hosting web-application at local instance"""
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect




app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123321'
app.config['MYSQL_DB'] = 'multilib_db'

mysql = MySQL(app)

@app.route('/')
@app.route('/main')
def main():
    """Main page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    data = cur.fetchall()
    cur.close()

    return render_template('main.html', categories=data )


@app.route("/items" , methods=['GET', 'POST'])
def items():
    """Items page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()

    cat_id = request.form.get("item-choice")
    cur.execute(f"SELECT  * FROM items WHERE item_category_id = {cat_id}")
    data_items = cur.fetchall()
    cur.close()


    return render_template('items.html', categories=categories_data,items=data_items)

@app.route("/item/<string:id_data>" , methods=['GET', 'POST'])
def item(id_data):
    """Item page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()

    cur.execute(f"SELECT  * FROM items WHERE item_id = {id_data}")
    data_item = cur.fetchall()
    cur.close()

    return render_template('item.html', categories=categories_data,items=data_item )

@app.route('/search')
def search():
    """Items page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()


    return render_template('search.html', categories=categories_data)


@app.route("/item/edit/<string:id_data>" , methods=['GET', 'POST'])
def edit_item(id_data=None):
    """Edit page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()

    if id_data is not None:
        cur.execute(f"SELECT  * FROM items WHERE item_id = {id_data}")
        data_item = cur.fetchall()
        cur.close()
        return render_template('edit_item.html', categories=categories_data,items=data_item)
    cur.close()

    return render_template('edit_item.html', categories=categories_data)



@app.route('/item/update' , methods=['GET', 'POST'])
def update_item():
    """Edit page function"""
    item_id = int(request.form["item-id"])
    item_category = int(request.form["item-category"])
    item_info = str(request.form["item-info"])
    item_label = str(request.form["item-label"])
    item_photo_link = str(request.form["item-photo-link"])
    item_video_link = str(request.form["item-video-link"])
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT category_id FROM categories WHERE category_id = {item_category};")
    categories_data = cur.fetchone()
    
    try:
        int(categories_data[0])
        cur.execute(f"UPDATE items SET item_category_id = {item_category}, item_label = '{item_label}', item_info = '{item_info}', item_video_link = '{item_video_link}', item_photo_link = '{item_photo_link}' WHERE item_id = {item_id};")
        mysql.connection.commit()
        cur.close()
        return redirect(f"http://127.0.0.1:5000/item/{item_id}")
    except:
        cur.close()
        return render_template('error.html')
    

@app.route('/error' , methods=['GET'])
def error():
    return render_template('error.html')
    
@app.route('/item/add_item' , methods=['GET'])
def add_item_item():
    """Edit page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()
    cur.close()

    return render_template('add_item.html', categories=categories_data)


@app.route('/item/adding' , methods=['GET', 'POST'])
def adding_item():
    """Edit page function"""
    category_id = int(request.form["item-choice"])
    item_info = str(request.form["item-info"])
    item_label = str(request.form["item-label"])
    item_photo_link = str(request.form["item-photo-link"])
    item_video_link = str(request.form["item-video-link"])
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT category_id FROM categories WHERE category_id = {category_id};")
    categories_data = cur.fetchone()
    try:
        int(categories_data[0])
        cur.execute(f"INSERT INTO Items (item_category_id,item_label,item_info,item_video_link,"
                    f"item_photo_link) VALUES ({category_id},'{item_label}','{item_info}',"
                    f"'{item_video_link}','{item_photo_link}');")
        mysql.connection.commit()
        cur.execute(f"SELECT item_id FROM items WHERE item_label = '{item_label}';")
        new_item_id = cur.fetchone()
        cur.close()
        return redirect(f"http://127.0.0.1:5000/item/{new_item_id[0]}")
    except:
        cur.close()
        return redirect(f"http://127.0.0.1:5000/error")

@app.route('/item/delete/<string:id_data>' , methods=['GET', 'POST'])
def delete_item(id_data):
    """Delete page function"""
    return render_template('delete_item.html', id_data=id_data)

@app.route('/item/deleting/<string:id_data>' , methods=['GET', 'POST'])
def deleting_item(id_data):
    """Deletein page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM items WHERE item_id={id_data};")
        mysql.connection.commit()
        cur.close()
        return redirect(f"http://127.0.0.1:5000/")
    except:
        cur.close()
        return render_template('error.html')
    


@app.route('/category/selection' , methods=['GET', 'POST'])
def selection_category():
    """Delete page function"""
    return render_template('selection.html')

@app.route('/category/create' , methods=['GET', 'POST'])
def add_category():
    """Delete page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()
    cur.close()

    return render_template('add_category.html', categories=categories_data)

@app.route('/category/adding' , methods=['GET', 'POST'])
def adding_category():
    """Delete page function"""
    category_label = str(request.form["category-label"])
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO categories (category_label) VALUES ('{category_label}');")
        mysql.connection.commit()
        cur.close()
        return redirect(f"http://127.0.0.1:5000/")
    except:
        return redirect(f"http://127.0.0.1:5000/error")


@app.route('/category/edit' , methods=['GET', 'POST'])
def edit_category():
    """Delete page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()
    cur.close()

    return render_template('edit_category.html', categories=categories_data)

@app.route('/category/update' , methods=['GET', 'POST'])
def update_category():
    """Edit page function"""
    category_id = int(request.form["category-id"])
    category_label = str(request.form["category-label"])
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE categories SET category_label = '{category_label}' WHERE category_id = {category_id};")
        mysql.connection.commit()
        cur.close()
        return redirect(f"http://127.0.0.1:5000/")
    except:
        return render_template('error.html')


@app.route('/category/delete' , methods=['GET', 'POST'])
def delete_category():
    """Delete page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    categories_data = cur.fetchall()
    cur.close()
    return render_template('delete_category.html', categories=categories_data)

@app.route('/category/delete-confirm' , methods=['GET', 'POST'])
def delete_confirm_category():
    """Delete page function"""
    category_id = int(request.args["category-id"])
    return render_template('delete_confirm_category.html', delete_id=category_id)




@app.route('/category/deleting/<int:delete_id>', methods=['GET', 'POST'])
def deliting_category(delete_id=None):
    """Delete page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM categories WHERE category_id={delete_id};")
        mysql.connection.commit()
        cur.close()
        return redirect(f"http://127.0.0.1:5000/")
    except:
        cur.close()
        return redirect(f"http://127.0.0.1:5000/error")















if __name__ == "__main__":
    app.run(debug=True)
