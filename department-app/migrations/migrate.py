import os

os.system('python ./department-app/migrations/000_create_database.py')
os.system('python ./department-app/migrations/001_create_categories_schema.py')
os.system('python ./department-app/migrations/002_create_items_schema.py')
os.system('python ./department-app/migrations/003_data_init.py')