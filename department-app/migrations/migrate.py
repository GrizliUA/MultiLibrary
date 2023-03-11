"""Module providing os functions"""
import os

os.system('python ./department-app/migrations/create_database.py')
os.system('python ./department-app/migrations/data_init.py')
