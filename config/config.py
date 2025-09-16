import os

# Ruta absoluta a la carpeta donde está app.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Base de datos en la raíz del proyecto
DATABASE = os.path.join(BASE_DIR, 'db.sqlite3')

DEBUG = True
SECRET_KEY = 'ia_model1234'