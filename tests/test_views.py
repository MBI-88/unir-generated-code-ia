from unittest.mock import patch
from src.models.task_model import Task

def test_index_view_empty(client):
    with patch.object(Task, "all", return_value=[]):
        response = client.get('/')
        assert response.status_code == 200
        html = response.data.decode()
        assert "No tasks yet" in html

def test_index_view_with_task(client):
    fake_task = Task(id=1, title="My Task")
    with patch.object(Task, "all", return_value=[fake_task]):
        response = client.get('/')
        html = response.data.decode()
        assert "My Task" in html
        assert "Edit" in html
        assert "Delete" in html

def test_form_view(client):
    response = client.get('/create')
    assert response.status_code == 200
    html = response.data.decode()
    assert "<form" in html
    assert "Title *" in html
    assert "Save Task" in html

def test_edit_view(client):
    fake_task = Task(id=1, title="Task to Edit")
    with patch.object(Task, "find", return_value=fake_task):
        response = client.get('/edit/1')
        assert response.status_code == 200
        html = response.data.decode()
        assert "Task to Edit" in html
        assert "Update Task" in html