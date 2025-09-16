import os
from flask import Flask
import config.config
from src.controllers.tasks_controller import task_bp
from src.models.taks_model import Task
import config

app = Flask(__name__)
app.config.from_object(config)

# Crear tabla si no existe
if not os.path.exists(config.config.DATABASE):
    print("Database not found. Creating...")
    Task.create_table()


# Registrar Blueprint
app.register_blueprint(task_bp)

if __name__ == '__main__':
    app.run(debug=config.config.DEBUG)