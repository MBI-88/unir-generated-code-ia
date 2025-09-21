from unittest.mock import patch
from src.models.task_model import Task

def test_index_route(client):
    with patch.object(Task, "all", return_value=[]):
        response = client.get('/')
        assert response.status_code == 200
        assert b"No tasks yet" in response.data

def test_create_task(client):
    with patch.object(Task, "save", return_value=None):
        response = client.post('/create', data={
            'title': 'Controller Task',
            'description': 'From controller test',
            'priority': 1
        }, follow_redirects=True)
        assert response.status_code == 200

def test_edit_task(client):
    fake_task = Task(id=1, title="Old Title")
    with patch.object(Task, "find", return_value=fake_task), \
         patch.object(Task, "update", return_value=None):
        response = client.post('/edit/1', data={
            'title': 'New Title',
            'status': 'completed',
            'priority': 2
        }, follow_redirects=True)
        assert response.status_code == 200

def test_delete_task(client):
    with patch.object(Task, "delete", return_value=None):
        response = client.post('/delete/1', follow_redirects=True)
        assert response.status_code == 200