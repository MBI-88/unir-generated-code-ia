from flask import Blueprint, render_template, request, redirect
from models.taks_model import insert_user, get_all_users

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def index():
    users = get_all_users()
    return render_template('index.html', users=users)

@user_bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        insert_user(name)
        return redirect('/')
    return render_template('form.html')