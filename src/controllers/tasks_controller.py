from flask import Blueprint, render_template, request, redirect, url_for
from src.models.taks_model import Task

task_bp = Blueprint('task_bp', __name__, template_folder="../views")

@task_bp.route('/')
def index():
    tasks = Task.all()
    return render_template('index.html', tasks=tasks)

@task_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        task = Task(
            title=request.form['title'],
            description=request.form.get('description'),
            due_date=request.form.get('due_date'),
            priority=int(request.form.get('priority', 2)),
            tags=request.form.get('tags')
        )
        task.save()
        return redirect(url_for('task_bp.index'))
    return render_template('form.html')

@task_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.find(task_id)
    if not task:
        return redirect(url_for('task_bp.index'))

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description')
        task.due_date = request.form.get('due_date')
        task.completed_at = request.form.get('completed_at') or None
        task.status = request.form.get('status', 'pending')
        task.priority = int(request.form.get('priority', 2))
        task.tags = request.form.get('tags')
        task.update()
        return redirect(url_for('task_bp.index'))

    return render_template('edit.html', task=task)

@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    Task.delete(task_id)
    return redirect(url_for('task_bp.index'))