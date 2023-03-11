"""Modules providing Flask realising hosting web-application at local instance"""
from flask_mysqldb import MySQL
from flask import Flask, render_template, request



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
    data_categories = cur.fetchall()

    cat_id = request.form.get("item-choice")
    cur.execute(f"SELECT  * FROM items WHERE item_category_id = {cat_id}")
    data_items = cur.fetchall()

    cur.close()

    return render_template('main.html', categories=data_categories,items=data_items )

@app.route("/item/<string:id_data>" , methods=['GET', 'POST'])
def item(id_data):
    """Item page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM categories")
    data_categories = cur.fetchall()

    cur.execute(f"SELECT  * FROM items WHERE item_id = {id_data}")
    data_item = cur.fetchall()
    print(data_item)

    cur.close()

    return render_template('product.html', categories=data_categories,items=data_item )
@app.route('/search')
def search():
    """Search page function"""
    return render_template("search.html")


@app.route('/auth')
def auth():
    """Auth page function"""
    return render_template("auth.html")


@app.route('/profile')
def profile():
    """Profile page function"""
    return render_template("profile.html")


@app.route('/product')
def product():
    """Product page function"""
    return render_template("product.html")


if __name__ == "__main__":
    app.run(debug=True)
