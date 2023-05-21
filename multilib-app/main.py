"""Modules providing Flask realising hosting web-application at local instance"""
from urllib.request import urlopen
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, make_response
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from datetime import datetime
from sqlalchemy import func 
from models.models import db, Categories, Items

import random
#pylint: disable=W0702
#pylint: disable=C0200



app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123321@localhost/multilib_db'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123321'
app.config['MYSQL_DB'] = 'multilib_db'

db.init_app(app)
mysql = MySQL(app)

app.app_context().push()
db.create_all()


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
def response_500(response='Internal Server Error'):
    """Returns response with code 500"""
    return make_response(response,500)

def obj_to_list(obj) -> list:
    new_list = []
    for row in obj:
        new_list.append(list((getattr(row, col)) for col in row.__table__.columns.keys()))
    return new_list


# category = Categories(category_label=random.randint(0, 10000))
# db.session.add(category)
# db.session.commit()
# item = Items(item_category_id=random.randint(0, 10),
#           item_label=random.randint(0, 10000))
# db.session.add(item)
# db.session.commit()

def category_response(categories_data):
    return {"category_id": categories_data[0][0], "category_label": categories_data[0][1]}

def item_response(item_data):
    return {"item_id": item_data[0][0],
            "item_category_id": item_data[0][1],
            "item_label": item_data[0][2],
            "item_info": item_data[0][3],
            "item_video_link": item_data[0][4],
            "item_photo_link": item_data[0][5],
            "item_date": item_data[0][6],
            "item_score": item_data[0][7]}




@app.route('/' , methods=['GET'])
def main():
    """Main page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())
        return render_template('main.html', title='Main', categories=categories_data)
    except:
        return redirect("http://127.0.0.1:5000/error")


@app.route("/items" , methods=['GET', 'POST'])
def items():
    """Items page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())
        item_category_id = request.form["item_category_id"]
        print(item_category_id)
        item_data = obj_to_list(Items.query.filter_by(item_category_id = item_category_id).all())

        return render_template('items.html', categories=categories_data, item_data=item_data,
                               item_category_id=item_category_id)
    except:
        return redirect("http://127.0.0.1:5000/error")

@app.route("/item/<int:id_data>" , methods=['GET', 'POST'])
def item(id_data):
    """Item page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())
        item_data = obj_to_list(Items.query.filter_by(item_id = int(id_data)).all())

        if not item_data:
            return redirect("http://127.0.0.1:5000/error")

        return render_template('item.html', categories=categories_data, items=item_data)
    except:
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/search', methods=['GET', 'POST'])
def item_search():
    """Search page function"""
    req=''
    if request.method == 'POST':
        req = request.form["item_label"]
    try:
        categories_data = obj_to_list(Categories.query.all())

        return render_template('search.html', categories=categories_data, writed_request=req)
    except:
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
    except:
        return redirect("http://127.0.0.1:5000/item/search")

@app.route("/item/edit/<int:id_data>" , methods=['GET', 'POST'])
def edit_item(id_data=None):
    """Edit page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())
        
        data_item = obj_to_list(Items.query.filter_by(item_id = int(id_data)).all())

        if id_data is not None:
            return render_template('edit_item.html', categories=categories_data,items=data_item)

        return render_template('edit_item.html', categories=categories_data)
    except:
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/update' , methods=['GET', 'POST'])
def update_item():
    """Edit page function"""
    try:
        item_data = db.session.get(Items, int(request.form["item_id"]))

        item_data.item_category_id = int(request.form["item_category_id"])
        item_data.item_label = str(request.form["item_label"])
        item_data.item_info = str(request.form["item_info"])
        item_data.item_video_link = str(request.form["item_video_link"])
        item_data.item_photo_link = str(request.form["item_photo_link"])
        if len(str(request.form["item_date"])) == 4:
            item_data.item_date = datetime(int(request.form["item_date"]),1,1)
        else:
            item_data.item_date = datetime(1970,1,1)

        if request.form["item_score"] == '':
            item_data.item_score = 0
        else:
            item_data.item_score = float(request.form["item_score"])
        db.session.flush()
        db.session.commit()
        return redirect(f"http://127.0.0.1:5000/item/{item_data.item_id}")
    except:
        db.session.rollback()
        return redirect("http://127.0.0.1:5000/error")


@app.route('/error' , methods=['GET'])
def error():
    """Error page function"""
    try:
        return render_template('error.html')
    except:
        return response_400()

@app.route('/item/add_item' , methods=['GET'])
def add_item_item():
    """Edit page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())

        return render_template('add_item.html', categories=categories_data)
    except:
        return redirect("http://127.0.0.1:5000/error")



@app.route('/item/adding' , methods=['GET', 'POST'])
def adding_item():
    """Edit page function"""
    try:
        try:
            new_item_id = obj_to_list(Items.query.filter_by(item_label = str(request.form["item_label"])).all())
            return redirect(f"http://127.0.0.1:5000/item/{new_item_id[0][0]}")
        except:
            if len(str(request.form["item_date"])) == 4:
                date = datetime(int(request.form["item_date"]),1,1)
            else:
                date = datetime(1970,1,1)

            if request.form["item_score"] == '':
                score = 0.0
            else:
                score = float(request.form["item_score"])

            item = Items(item_category_id=int(request.form["item_category_id"]),
                        item_label=str(request.form["item_label"]),
                        item_info=str(request.form["item_info"]),
                        item_video_link=str(request.form["item_video_link"]),
                        item_photo_link=str(request.form["item_photo_link"]),
                        item_date=date,
                        item_score=score)
            db.session.add(item)
            db.session.commit()
            new_item_id = obj_to_list(Items.query.filter_by(item_label = str(request.form["item_label"])).all())

            return redirect(f"http://127.0.0.1:5000/item/{new_item_id[0][0]}")
    except:
        db.session.rollback()
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/delete/<string:id_data>' , methods=['GET', 'POST'])
def delete_item(id_data):
    """Delete page function"""
    try:
        return render_template('delete_item.html', id_data=id_data)
    except:
        return redirect("http://127.0.0.1:5000/error")

@app.route('/item/deleting/<string:id_data>' , methods=['GET', 'POST'])
def deleting_item(id_data):
    """Deleting page function"""
    try:
        Items.query.filter_by(item_id=id_data).delete()
        db.session.commit()
        return redirect("http://127.0.0.1:5000/")
    except:
        db.session.rollback()
        return render_template('error.html')



@app.route('/category/selection' , methods=['GET', 'POST'])
def selection_category():
    """Delete page function"""
    try:
        return render_template('selection.html')
    except:
        return redirect("http://127.0.0.1:5000/error")

@app.route('/category/create' , methods=['GET', 'POST'])
def add_category():
    """Delete page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())

        return render_template('add_category.html', categories=categories_data)
    except:
        return redirect("http://127.0.0.1:5000/error")

@app.route('/category/adding' , methods=['GET', 'POST'])
def adding_category():
    """Delete page function"""
    try:
        category = Categories(category_label=str(request.form["category-label"]))
        db.session.add(category)
        db.session.commit()

        return redirect("http://127.0.0.1:5000/")
    except:
        db.session.rollback()
        return redirect("http://127.0.0.1:5000/error")


@app.route('/category/edit' , methods=['GET', 'POST'])
def edit_category():
    """Delete page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())

        return render_template('edit_category.html', categories=categories_data)
    except:
        return redirect("http://127.0.0.1:5000/error")




@app.route('/category/update' , methods=['GET', 'POST'])
def update_category():
    """Edit page function"""
    try:
        category_data = db.session.get(Categories, int(request.form["category-id"]))
        category_data.category_label = str(request.form["category-label"])
        db.session.commit()

        return redirect("http://127.0.0.1:5000/")
    except:
        db.session.rollback()
        return redirect("http://127.0.0.1:5000/error")


@app.route('/category/delete' , methods=['GET', 'POST'])
def delete_category():
    """Delete page function"""
    try:
        categories_data = obj_to_list(Categories.query.all())

        return render_template('delete_category.html', categories=categories_data)
    except:
        return redirect("http://127.0.0.1:5000/error")


@app.route('/category/delete-confirm' , methods=['GET', 'POST'])
def delete_confirm_category():
    """Delete page function"""
    try:
        category_id = int(request.form["category-id"])

        return render_template('delete_confirm_category.html', delete_id=category_id)
    except:
        return redirect("http://127.0.0.1:5000/error")



@app.route('/category/deleting/<int:delete_id>', methods=['GET', 'POST'])
def deliting_category(delete_id=None):
    """Delete page function"""
    try:
        Categories.query.filter_by(category_id=delete_id).delete()
        db.session.commit()
        return redirect("http://127.0.0.1:5000/")
    except:
        db.session.rollback()
        return redirect("http://127.0.0.1:5000/error")



class ApiCategoryCreate(Resource):
    """Category API Create realization"""
    def post(self):
        """API Category Create"""
        try:
            category_request = request.args['category_label']
            category = Categories(category_label=category_request)
            db.session.add(category)
            db.session.flush()
            db.session.commit()

            categories_data = obj_to_list(Categories.query.filter_by(category_label = category_request).all())

            response = category_response(categories_data)
            return response_201(response)
        except:
            try:
                db.session.rollback()

                categories_data = obj_to_list(Categories.query.filter_by(category_label = category_request).all())

                response = category_response(categories_data)
                return response_208(response)
            except:
                db.session.rollback()
                return response_500()
api.add_resource(ApiCategoryCreate, '/api/category/create/')


class ApiCategoryRead(Resource):
    """Category API Read realization"""
    def get(self):
        """API Category Read"""
        try:
            category_id = request.args['category_id']
            categories_data = obj_to_list(Categories.query.filter_by(category_id = category_id).all())
        except:
            try:
                category_label = request.args['category_label']
                categories_data = obj_to_list(Categories.query.filter_by(category_label = category_label).all())
            except:
                return response_400()
        try:
            if len(categories_data) == 1:
                response = category_response(categories_data)
                return response_200(response)
            else:
                return response_400()
        except:
            return response_500()
api.add_resource(ApiCategoryRead, '/api/category/read/')


class ApiCategoryUpdate(Resource):
    """Category API Update realization"""
    def put(self):
        """API Category Update"""
        try:
            try:
                category_data = db.session.get(Categories, request.args["category_id"])
                category_data.category_label = request.args['category_label']
                db.session.commit()
                return response_202()
            except:
                db.session.rollback()
                return response_400()
        except:
            db.session.rollback()
            return response_500()
api.add_resource(ApiCategoryUpdate, '/api/category/update/')


class ApiCategoryDelete(Resource):
    """Category API Delete realization"""
    def delete(self):
        """API Category Delete"""
        try:
            category_id = request.args['category_id']
            Categories.query.filter_by(category_id=category_id).delete()
        except:
            try:
                category_label = request.args['category_label']
                Categories.query.filter_by(category_label=category_label).delete()
            except:
                return response_400()
        try:
            db.session.commit()
            return response_202()
        except:
            return response_500()
api.add_resource(ApiCategoryDelete, '/api/category/delete/')



class ApiItemCreate(Resource):
    """Item API Create realization"""
    def post(self):
        """API Category Create"""
        try:
            data = ''
            for key, value in request.args.items():
                data += f'{key} = "{value}", '
            data = data[:-2]

            item = Items(**eval('dict(' + data + ')'))

            db.session.add(item)
            db.session.flush()
            db.session.commit()

            item_data = obj_to_list(Items.query.filter_by(**eval('dict(' + data + ')')).all())

            response = item_response(item_data)
            return response_201(response)
        except:
            try:
                db.session.rollback()
                item_data = obj_to_list(Items.query.filter_by(**eval('dict(' + data + ')')).all())

                response = item_response(item_data)
                return response_208(response)
            except:
                db.session.rollback()
                return response_500()
api.add_resource(ApiItemCreate, '/api/item/create/')


class ApiItemRead(Resource):
    """Item API Read realization"""
    def get(self):
        """API Item Read"""
        try:
            item_data = obj_to_list(Items.query.filter_by(item_id = int(request.args['item_id'])).all())
        except:
            try:
                item_data = obj_to_list(Items.query.filter_by(item_label = request.args['item_label']).all())
            except:
                return response_400()
        try:
            if len(item_data) == 1:
                response = item_response(item_data)
                return response_200(response)
            else:
                return response_400()
        except:
            return response_500()
api.add_resource(ApiItemRead, '/api/item/read/')


class ApiItemUpdate(Resource):
    """Item API Update realization"""
    def put(self):
        """API Item Update"""
        try:
            item_data = db.session.get(Items, int(request.args["item_id"]))
            try:
                if 'item_category_id' in request.args:
                    item_data.item_category_id = int(request.args['item_category_id'])
                if 'item_label' in request.args:
                    item_data.item_label = str(request.args['item_label'])
                if 'item_info' in request.args:
                    item_data.item_info = str(request.args['item_info'])
                if 'item_video_link' in request.args:
                    item_data.item_video_link = str(request.args['item_video_link'])
                if 'item_photo_link' in request.args:
                    item_data.item_photo_link = str(request.args['item_photo_link'])
                if 'item_date' in request.args:
                    date_parts = request.args["item_date"].split(',')
                    if len(date_parts) == 3:
                        year, month, day = map(int, date_parts)
                        item_data.item_date = datetime(year, month, day)
                    else:
                        item_data.item_date = datetime(1970,1,1)
                if 'item_score' in request.args:
                    item_data.item_score = float(request.args['item_score'])

                db.session.add(item_data)
                db.session.flush()
                db.session.commit()

                item_data = obj_to_list(Items.query.filter_by(item_id = int(request.args['item_id'])).all())

                response = item_response(item_data)
                return response_202(response)
            except:
                db.session.rollback()
                return response_400()
        except:
            db.session.rollback()
            return response_500()
api.add_resource(ApiItemUpdate, '/api/item/update/')


class ApiItemDelete(Resource):
    """Item API Delete realization"""
    def delete(self):
        """API Item Delete"""
        try:
            item_id = request.args['item_id']
            Items.query.filter_by(item_id=item_id).delete()
        except:
            try:
                item_label = request.args['item_label']
                Items.query.filter_by(item_label=item_label).delete()
            except:
                return response_400()
        try:
            db.session.commit()
            return response_202()
        except:
            return response_500()
api.add_resource(ApiItemDelete, '/api/item/delete/')


class ApiItemSearch(Resource):
    """Item API Search realization"""
    def get(self):
        """API Item Search"""
        try:
            data = ''

            for key, value in request.args.items():
                data += f'{key} = "{value}", '
            data = data[:-2]

            if data == '':
                return response_400()
            

            item_data = obj_to_list(Items.query.filter_by(**eval('dict(' + data + ')')).all())

            if not item_data:
                return response_404()

            response = item_response(item_data)

            return response_200(response)
        except:
            return response_400()
api.add_resource(ApiItemSearch, '/api/item/search/')



if __name__ == "__main__":
    # handler = RotatingFileHandler('./multilib-app/debug.log', maxBytes=1000000, backupCount=1)
    # handler.setLevel(logging.DEBUG)
    # app.logger.addHandler(handler)
    # log = logging.getLogger('werkzeug')
    # log.setLevel(logging.DEBUG)
    # frmt = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')
    # handler.setFormatter(frmt)
    # log.addHandler(handler)
    app.run(host='0.0.0.0', debug=True)
