from flask_sqlalchemy import SQLAlchemy
import datetime as dt

db = SQLAlchemy()
class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    category_label = db.Column(db.String(100), nullable=False, unique=True)

    
class Items(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    item_label = db.Column(db.String(200), nullable=False, unique=True)

    item_info = db.Column(db.Text, nullable=True, default='')
    item_video_link = db.Column(db.String(255), nullable=True, default='')
    item_photo_link = db.Column(db.String(255), nullable=True, default='')
    item_date = db.Column(db.Date, nullable=True, default=dt.date(1970,1,1))
    item_score = db.Column(db.Float, nullable=True, default=0.0)