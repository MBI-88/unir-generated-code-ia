import os
from flask import Flask
import config.config
from src.controllers.tasks_controller import task_bp
from src.models.task_model import Task
import config

app = Flask(__name__)
app.config.from_object(config)
Task.create_table()


# Registrar Blueprint
app.register_blueprint(task_bp)

if __name__ == '__main__':
    app.run(debug=config.config.DEBUG)