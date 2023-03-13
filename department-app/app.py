"""Modules providing Flask realising hosting web-application at local instance"""
from urllib.request import urlopen
import json
import logging
from logging.handlers import RotatingFileHandler
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
    """Returns response with code 200"""
    return make_response(response,200)
def response_201(response='Created'):
    """Returns response with code 201"""
    return make_response(response,201)
def response_202(response='Accepted'):
    """Returns response with code 202"""
    return make_response(response,202)
def response_208(response='Already Reported'):
    """Returns response with code 208"""
    return make_response(response,208)
def response_400(response='Bad Request'):
    """Returns response with code 400"""
    return make_response(response,400)
def response_404(response='Not Found'):
    """Returns response with code 404"""
    return make_response(response,404)


@app.route('/')
def main():
    """Main page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        categories_data = cur.fetchall()
        cur.close()

        return render_template('main.html', categories=categories_data)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")


@app.route("/items" , methods=['GET', 'POST'])
def items():
    """Items page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        categories_data = cur.fetchall()

        item_category_id = request.form["item_category_id"]
        cur.execute(f"SELECT * FROM items WHERE item_category_id = {item_category_id}")

        item_data = cur.fetchall()
        cur.close()

        return render_template('items.html', categories=categories_data, item_data=item_data,
                               item_category_id=item_category_id)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")

@app.route("/item/<string:id_data>" , methods=['GET', 'POST'])
def item(id_data):
    """Item page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        categories_data = cur.fetchall()

        cur.execute(f"SELECT * FROM items WHERE item_id = {id_data}")
        item_data = cur.fetchall()
        cur.close()

        if not item_data:
            return redirect("http://127.0.0.1:5000/error")

        return render_template('item.html', categories=categories_data,items=item_data)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/search', methods=['GET', 'POST'])
def item_search():
    """Search page function"""
    req=''
    if request.method == 'POST':
        req = request.form["item_label"]
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        categories_data = cur.fetchall()
        cur.close()

        return render_template('search.html', categories=categories_data, writed_request=req)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/searching', methods=['GET', 'POST'])
def item_searching():
    """Search page function"""
    try:
        item_label = '?item_label=' + request.form["item_label"]
        item_date = '&item_date=' + request.form["item_date"]
        url = f"http://127.0.0.1:5000/api/item/search/{item_label+item_date}"

        with urlopen(url) as req:
            res = req.read()
        dict_res = json.loads(res)
        values_list = list(dict_res.values())

        return redirect(f"http://127.0.0.1:5000/item/{values_list[2]}")
    except (Exception,):
        return redirect("http://127.0.0.1:5000/item/search")

@app.route("/item/edit/<string:id_data>" , methods=['GET', 'POST'])
def edit_item(id_data=None):
    """Edit page function"""
    try:
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
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")



@app.route('/item/update' , methods=['GET', 'POST'])
def update_item():
    """Edit page function"""
    try:
        item_id = int(request.form["item_id"])

        item_update = ''
        for key, value in request.form.items():
            item_update += f"{key} = '{value}' , "
        item_update = item_update[15+len(str(item_id)):-3]

        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE items SET {item_update} WHERE item_id = {item_id};")
        mysql.connection.commit()
        cur.close()

        return redirect(f"http://127.0.0.1:5000/item/{item_id}")
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")


@app.route('/error' , methods=['GET'])
def error():
    """Error page function"""
    try:
        return render_template('error.html')
    except (Exception,):
        return response_400()

@app.route('/item/add_item' , methods=['GET'])
def add_item_item():
    """Edit page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        categories_data = cur.fetchall()
        cur.close()

        return render_template('add_item.html', categories=categories_data)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")


@app.route('/item/adding' , methods=['GET', 'POST'])
def adding_item():
    """Edit page function"""
    try:
        item_category_id = int(request.form["item_category_id"])
        item_label = str(request.form["item_label"])
        item_info = str(request.form["item_info"])
        item_video_link = str(request.form["item_video_link"])
        item_photo_link = str(request.form["item_photo_link"])
        item_date = str(request.form["item_date"])
        item_value = str(request.form["item_value"])

        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO Items (item_category_id,item_label,item_info,item_video_link,"
                    f"item_photo_link,item_date,item_value) VALUES ({item_category_id},"
                    f"'{item_label}','{item_info}','{item_video_link}','{item_photo_link}',"
                    f"'{item_date}','{item_value}');")
        mysql.connection.commit()
        cur.execute(f"SELECT item_id FROM items WHERE item_label = '{item_label}';")
        new_item_id = cur.fetchone()
        cur.close()

        return redirect(f"http://127.0.0.1:5000/item/{new_item_id[0]}")
    except (Exception,):
        cur.close()
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/delete/<string:id_data>' , methods=['GET', 'POST'])
def delete_item(id_data):
    """Delete page function"""
    try:
        return render_template('delete_item.html', id_data=id_data)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/deleting/<string:id_data>' , methods=['GET', 'POST'])
def deleting_item(id_data):
    """Deleting page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM items WHERE item_id={id_data};")
        mysql.connection.commit()
        cur.close()
        return redirect("http://127.0.0.1:5000/")
    except (Exception,):
        cur.close()
        return render_template('error.html')



@app.route('/category/selection' , methods=['GET', 'POST'])
def selection_category():
    """Delete page function"""
    try:
        return render_template('selection.html')
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")

@app.route('/category/create' , methods=['GET', 'POST'])
def add_category():
    """Delete page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM categories")
        categories_data = cur.fetchall()
        cur.close()

        return render_template('add_category.html', categories=categories_data)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")

@app.route('/category/adding' , methods=['GET', 'POST'])
def adding_category():
    """Delete page function"""
    try:
        category_label = str(request.form["category-label"])
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO categories (category_label) VALUES ('{category_label}');")
        mysql.connection.commit()
        cur.close()
        return redirect("http://127.0.0.1:5000/")
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")


@app.route('/category/edit' , methods=['GET', 'POST'])
def edit_category():
    """Delete page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM categories")
        categories_data = cur.fetchall()
        cur.close()

        return render_template('edit_category.html', categories=categories_data)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")




@app.route('/category/update' , methods=['GET', 'POST'])
def update_category():
    """Edit page function"""
    try:
        category_id = int(request.form["category-id"])
        category_label = str(request.form["category-label"])

        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE categories SET category_label = '{category_label}'"
                    f" WHERE category_id = {category_id};")
        mysql.connection.commit()
        cur.close()

        return redirect("http://127.0.0.1:5000/")
    except (Exception,):
        return render_template('error.html')


@app.route('/category/delete' , methods=['GET', 'POST'])
def delete_category():
    """Delete page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM categories")
        categories_data = cur.fetchall()
        cur.close()

        return render_template('delete_category.html', categories=categories_data)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")


@app.route('/category/delete-confirm' , methods=['GET', 'POST'])
def delete_confirm_category():
    """Delete page function"""
    try:
        category_id = int(request.form["category-id"])

        return render_template('delete_confirm_category.html', delete_id=category_id)
    except (Exception,):
        return redirect("http://127.0.0.1:5000/error")



@app.route('/category/deleting/<int:delete_id>', methods=['GET', 'POST'])
def deliting_category(delete_id=None):
    """Delete page function"""
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM categories WHERE category_id={delete_id};")
        mysql.connection.commit()
        cur.close()
        return redirect("http://127.0.0.1:5000/")
    except (Exception,):
        cur.close()
        return redirect("http://127.0.0.1:5000/error")























class ApiCategoryCreate(Resource):
    """Category API Create realization"""
    def post(self,category_label):
        """API Category Create"""
        try:
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO categories (category_label) VALUES ('{category_label}');")
            mysql.connection.commit()

            cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}'")
            categories_data = cur.fetchone()
            cur.close()

            response = {"category_id": categories_data[0], "category_label": categories_data[1]}
            return response_201(response)
        except (Exception,):
            try:
                cur = mysql.connection.cursor()
                cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}'")
                categories_data = cur.fetchone()
                cur.close()

                response = {"category_id": categories_data[0], "category_label": categories_data[1]}
                return response_208(response)
            except (Exception,):
                return response_400()
api.add_resource(ApiCategoryCreate, '/api/category/create/<string:category_label>')


class ApiCategoryRead(Resource):
    """Category API Read realization"""
    def get(self,category_request):
        """API Category Read"""
        try:
            category_request = int(category_request)
        except (Exception,):
            pass
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
        except (Exception,):
            return response_400()
api.add_resource(ApiCategoryRead, '/api/category/read/<string:category_request>')


class ApiCategoryUpdate(Resource):
    """Category API Update realization"""
    def put(self,category_request):
        """API Category Update"""
        try:
            category_request = int(category_request)
        except (Exception,):
            pass
        try:
            category_label = str(request.args["category_label"])
            cur = mysql.connection.cursor()

            if isinstance(category_request,int):
                cur.execute(f"UPDATE categories SET category_label = '{category_label}'"
                            f"WHERE category_id = {category_request};")
                mysql.connection.commit()
                cur.execute(f"SELECT * FROM categories WHERE category_id = {category_request}")
            else:
                cur.execute(f"UPDATE categories SET category_label = '{category_label}'"
                            f"WHERE category_label = '{category_request}';")
                mysql.connection.commit()
                cur.execute(f"SELECT * FROM categories WHERE category_label = '{category_label}';")

            categories_data = cur.fetchone()
            cur.close()

            response = {"category_id": categories_data[0], "category_label": categories_data[1]}
            return response_202(response)
        except (Exception,):
            return response_400()
api.add_resource(ApiCategoryUpdate, '/api/category/update/<string:category_request>')


class ApiCategoryDelete(Resource):
    """Category API Delete realization"""
    def delete(self,category_request):
        """API Category Delete"""
        try:
            category_request = int(category_request)
        except (Exception,):
            pass
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
        except (Exception,):
            return response_400()
api.add_resource(ApiCategoryDelete, '/api/category/delete/<string:category_request>')



class ApiItemCreate(Resource):
    """Item API Create realization"""
    def post(self):
        """API Item Create"""
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
        except (Exception,):
            return response_400()
api.add_resource(ApiItemCreate, '/api/item/create/')


class ApiItemRead(Resource):
    """Item API Read realization"""
    def get(self,item_request):
        """API Item Read"""
        try:
            item_request = int(item_request)
        except (Exception,):
            pass
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
        except (Exception,):
            return response_400()
api.add_resource(ApiItemRead, '/api/item/read/<string:item_request>')


class ApiItemUpdate(Resource):
    """Item API Update realization"""
    def put(self,item_request):
        """API Item Update"""
        try:
            item_request = int(item_request)
        except (Exception,):
            pass
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
        except (Exception,):
            return response_400()
api.add_resource(ApiItemUpdate, '/api/item/update/<string:item_request>')


class ApiItemDelete(Resource):
    """Item API Delete realization"""
    def delete(self,item_request):
        """API Item Delete"""
        try:
            item_request = int(item_request)
        except (Exception,):
            pass
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
        except (Exception,):
            return response_400()
api.add_resource(ApiItemDelete, '/api/item/delete/<string:item_request>')


class ApiItemSearch(Resource):
    """Item API Search realization"""
    def get(self):
        """API Item Search"""
        try:
            item_keys,item_values = [],[]
            for key, value in request.args.items():
                item_keys.append(key)
                item_values.append(value)

            cur = mysql.connection.cursor()
            if not item_keys:
                return response_400()

            for i in range(0,len(item_keys)):
                cur.execute(f"SELECT * FROM items WHERE {item_keys[i]} = '{item_values[i]}';")
                item_data = cur.fetchone()
                if item_data:
                    break

            if not item_data:
                return response_404()
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
        except (Exception,):
            return response_400()
api.add_resource(ApiItemSearch, '/api/item/search/')



if __name__ == "__main__":
    handler = RotatingFileHandler('./department-app/debug.log', maxBytes=1000000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    frmt = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')
    handler.setFormatter(frmt)
    log.addHandler(handler)
    app.run(host='0.0.0.0', debug=True)
