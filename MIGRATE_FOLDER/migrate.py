import os

os.system('python ./MIGRATE_FOLDER/000_create_database.py')
os.system('python ./MIGRATE_FOLDER/001_create_categories_schema.py')
os.system('python ./MIGRATE_FOLDER/002_create_items_schema.py')
os.system('python ./MIGRATE_FOLDER/003_data_init.py')