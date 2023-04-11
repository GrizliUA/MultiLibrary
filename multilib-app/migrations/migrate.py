"""Module providing os functions"""
import os

os.system('python ./multilib-app/migrations/create_database.py')
os.system('python ./multilib-app/migrations/data_init.py')
