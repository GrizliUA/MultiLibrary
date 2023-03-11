"""Module providing os functions"""
import os

os.system('python ./department-app/migrations/create_database.py')
os.system('python ./department-app/migrations/create_categories_schema.py')
os.system('python ./department-app/migrations/create_items_schema.py')
os.system('python ./department-app/migrations/data_init.py')
