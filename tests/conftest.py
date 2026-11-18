import os

# las pruebas usan sqlite en memoria para no tocar la base de mysql
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
