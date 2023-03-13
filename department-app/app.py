"""Modules providing Flask realising hosting web-application at local instance"""
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, make_response
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123321'
app.config['MYSQL_DB'] = 'multilib_db'

mysql = MySQL(app)

def response_200(response='OK'):
    return make_response(response,200)
def response_201(response='Created'):
    return make_response(response,201)
def response_202(response='Accepted'):
    return make_response(response,202)
def response_208(response='Already Reported'):
    return make_response(response,208)
def response_400(response='Bad Request'):
    return make_response(response,400)


@app.route('/')
@app.route('/main')
def main():
    """Main page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    data = cur.fetchall()
    cur.close()

    return render_template('main.html', categories=data )


@app.route("/items" , methods=['GET', 'POST'])
def items():
    """Items page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    categories_data = cur.fetchall()

    
    print(categories_data)
    item_category_id = request.form.get("item_category_id")
    print(item_category_id)
    cur.execute(f"SELECT * FROM items WHERE item_category_id = {item_category_id}")
    item_data = cur.fetchall()
    cur.close()


    return render_template('items.html', categories=categories_data,items=item_data)

@app.route("/item/<string:id_data>" , methods=['GET', 'POST'])
def item(id_data):
    """Item page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    categories_data = cur.fetchall()

    cur.execute(f"SELECT * FROM items WHERE item_id = {id_data}")
    item_data = cur.fetchall()
    cur.close()

    if not len(item_data):
        return redirect(f"http://127.0.0.1:5000/error")

    return render_template('item.html', categories=categories_data,items=item_data)

@app.route('/search')
def search():
    """Items page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    categories_data = cur.fetchall()


    return render_template('search.html', categories=categories_data)


@app.route("/item/edit/<string:id_data>" , methods=['GET', 'POST'])
def edit_item(id_data=None):
    """Edit page function"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    categories_data = cur.fetchall()

    if id_data is not None:
        cur.execute(f"SELECT * FROM items WHERE item_id = {id_data}")
        data_item = cur.fetchall()
        cur.close()
        return render_template('edit_item.html', categories=categories_data,items=data_item)
    cur.close()

    return render_template('edit_item.html', categories=categories_data)



@app.route('/item/update' , methods=['GET', 'POST'])
def update_item():
    """Edit page function"""
    try:
        item_id = int(request.form["item_id"])
        item_category_id = int(request.form["item_category_id"])
        item_update = ''
        for key, value in request.form.items():
            item_update += f"{key} = '{value}' , "
        item_update = item_update[15+len(str(item_id)):-3]

        cur = mysql.connection.cursor()
        cur.execute(f"SELECT category_id FROM categories WHERE category_id = {item_category_id};")
        categories_data = cur.fetchone()
    
        int(categories_data[0])
        cur.execute(f"UPDATE items SET {item_update} WHERE item_id = {item_id};")
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
    cur.execute("SELECT * FROM categories")
    categories_data = cur.fetchall()
    cur.close()

    return render_template('add_item.html', categories=categories_data)


@app.route('/item/adding' , methods=['GET', 'POST'])
def adding_item():
    """Edit page function"""
    item_category_id = int(request.form["item_category_id"])
    item_label = str(request.form["item_label"])
    item_info = str(request.form["item_info"])
    item_video_link = str(request.form["item_video_link"])
    item_photo_link = str(request.form["item_photo_link"])
    item_date = str(request.form["item_date"])
    item_value = str(request.form["item_value"])
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT category_id FROM categories WHERE category_id = {item_category_id};")
    categories_data = cur.fetchone()
    try:
        int(categories_data[0])
        cur.execute(f"INSERT INTO Items (item_category_id,item_label,item_info,item_video_link,"
                    f"item_photo_link,item_date,item_value) VALUES ({item_category_id},"
                    f"'{item_label}','{item_info}','{item_video_link}','{item_photo_link}',"
                    f"'{item_date}','{item_value}');")
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
    category_id = int(request.form["category-id"])
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























class api_category_create(Resource):
    def post(self,category_label):
        """Delete page function"""
        try:
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO categories (category_label) VALUES ('{category_label}');")
            mysql.connection.commit()

            cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}'")
            categories_data = cur.fetchone()
            cur.close()

            response = {"category_id": categories_data[0], "category_label": categories_data[1]}
            return response_201(response)
        except:
            try:
                cur = mysql.connection.cursor()
                cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}'")
                categories_data = cur.fetchone()
                cur.close()

                response = {"category_id": categories_data[0], "category_label": categories_data[1]}
                return response_208(response)
            except:
                return response_400()
api.add_resource(api_category_create, '/api/category/create/<string:category_label>')

class api_category_read(Resource):
    def get(self,category_request):
        """Delete page function"""
        try:
            category_request = int(category_request)
        except:pass
        try:
            cur = mysql.connection.cursor()
            if isinstance(category_request,int):
                cur.execute(f"SELECT * FROM categories WHERE category_id = '{category_request}'")
            else: 
                cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_request}'")
            categories_data = cur.fetchone()
            cur.close()

            response = {"category_id": categories_data[0], "category_label": categories_data[1]}
            return response_200(response)
        except:
            return response_400()
api.add_resource(api_category_read, '/api/category/read/<string:category_request>')

class api_category_update(Resource):
    def put(self,category_request):
        """Delete page function"""
        try:
            category_request = int(category_request)
        except:pass
        try:
            category_label = str(request.args["category_label"])
            cur = mysql.connection.cursor()

            if isinstance(category_request,int):
                cur.execute(f"UPDATE categories SET category_label = '{category_label}' WHERE category_id = {category_request};")
                mysql.connection.commit()
                cur.execute(f"SELECT * FROM categories WHERE category_id = {category_request}")
            else:
                cur.execute(f"UPDATE categories SET category_label = '{category_label}' WHERE category_label = '{category_request}';")
                mysql.connection.commit()
                cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}';")

            categories_data = cur.fetchone()
            cur.close()

            response = {"category_id": categories_data[0], "category_label": categories_data[1]}
            return response_202(response)
        except:
            return response_400()
api.add_resource(api_category_update, '/api/category/update/<string:category_request>')

class api_category_delete(Resource):
    def delete(self,category_request):
        """Delete page function"""
        try:
            category_request = int(category_request)
        except:pass
        try:
            cur = mysql.connection.cursor()

            if isinstance(category_request,int):
                cur.execute(f"DELETE FROM categories WHERE category_id = {category_request};")
                mysql.connection.commit()
            else: 
                cur.execute(f"DELETE FROM categories WHERE category_label = '{category_request}';")
                mysql.connection.commit()
            cur.close()

            return response_202()
        except:
            return response_400()
api.add_resource(api_category_delete, '/api/category/delete/<string:category_request>')



class api_item_create(Resource):
    def post(self):
        """Delete page function"""
        try:
            item_label = request.args['item_label']

            request_keys,request_values = '',''
            for key, value in request.args.items():
                request_keys += f'{key} , '
                request_values += f"'{value}' , "
            request_keys = request_keys[:-3]
            request_values = request_values[:-3]

            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO items ({request_keys}) VALUES ({request_values});")
            mysql.connection.commit()

            cur.execute(f"SELECT * FROM items WHERE item_label = '{item_label}'")
            item_data = cur.fetchone()
            cur.close()

            response = {"item_id": item_data[0],
                        "item_category_id": item_data[1],
                        "item_label": item_data[2],
                        "item_info": item_data[3],
                        "item_video_link": item_data[4],
                        "item_photo_link": item_data[5],
                        "item_date": item_data[6],
                        "item_value": item_data[7]}
            return response_201(response)
        except:
            return response_400()
api.add_resource(api_item_create, '/api/item/create/')

class api_item_read(Resource):
    def get(self,item_request):
        """Delete page function"""
        try:
            item_request = int(item_request)
        except:pass
        try:
            cur = mysql.connection.cursor()

            if isinstance(item_request,int):
                cur.execute(f"SELECT * FROM items WHERE item_id = '{item_request}'")
            else:
                cur.execute(f"SELECT * FROM items WHERE item_label = '{item_request}'")

            item_data = cur.fetchone()
            cur.close()

            response = {"item_id": item_data[0],
                        "item_category_id": item_data[1],
                        "item_label": item_data[2],
                        "item_info": item_data[3],
                        "item_video_link": item_data[4],
                        "item_photo_link": item_data[5],
                        "item_date": item_data[6],
                        "item_value": item_data[7]}
            return response_200(response)
        except:
            return response_400()
api.add_resource(api_item_read, '/api/item/read/<string:item_request>')

class api_item_update(Resource):
    def put(self,item_request):
        """Delete page function"""
        try:
            item_request = int(item_request)
        except:pass
        try:
            item_label = request.args['item_label']
            item_update = ''
            for key, value in request.args.items():
                item_update += f"{key} = '{value}' , "
            item_update = item_update[:-3]

            cur = mysql.connection.cursor()

            if isinstance(item_request,int):
                cur.execute(f"UPDATE items SET {item_update} WHERE item_id = '{item_request}';")
                mysql.connection.commit()
                cur.execute(f"SELECT * FROM items WHERE item_label = '{item_label}';")
            else:
                cur.execute(f"UPDATE items SET {item_update} WHERE item_label = '{item_request}';")
                mysql.connection.commit()
                cur.execute(f"SELECT * FROM items WHERE item_label = '{item_label}';")

            item_data = cur.fetchone()
            response = {"item_id": item_data[0],
                        "item_category_id": item_data[1],
                        "item_label": item_data[2],
                        "item_info": item_data[3],
                        "item_video_link": item_data[4],
                        "item_photo_link": item_data[5],
                        "item_date": item_data[6],
                        "item_value": item_data[7]}
            cur.close()
            return response_200(response)
        except:
            return response_400()
api.add_resource(api_item_update, '/api/item/update/<string:item_request>')

class api_item_delete(Resource):
    def delete(self,item_request):
        """Delete page function"""
        try:
            item_request = int(item_request)
        except:pass
        try:
            cur = mysql.connection.cursor()

            if isinstance(item_request,int):
                cur.execute(f"DELETE FROM items WHERE item_id = {item_request};")
            elif isinstance(item_request,str):
                cur.execute(f"DELETE FROM items WHERE item_label = '{item_request}';")
                return response_400()
            else: return response_400()

            mysql.connection.commit()
            return response_202()
        except:
            return response_400()
api.add_resource(api_item_delete, '/api/item/delete/<string:item_request>')














if __name__ == "__main__":
    app.run(debug=True)
