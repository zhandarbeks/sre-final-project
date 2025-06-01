# test_app.py
import pytest
import json
from app import app as flask_app # Import your Flask app object from app.py

@pytest.fixture
def app():
    # Reset todos for each test
    flask_app.config['TESTING'] = True
    global todos, todo_id_counter
    from app import todos as app_todos, todo_id_counter as app_todo_id_counter
    
    # Reference the global todos and counter from app.py
    # This is a simple way for testing; in a real app, you'd manage state better.
    _original_todos = app_todos[:]
    _original_counter = app_todo_id_counter
    
    app_todos.clear()
    globals()['todo_id_counter'] = 0 # Reset counter in the app module

    yield flask_app
    
    # Restore original state after test (optional, but good practice)
    app_todos[:] = _original_todos
    globals()['todo_id_counter'] = _original_counter


@pytest.fixture
def client(app):
    return app.test_client()

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the SRE To-Do List API!" in response.data

def test_add_and_get_todos(client):
    # Add a todo
    response_post = client.post('/todos', json={'task': 'Test the API'})
    assert response_post.status_code == 201
    assert response_post.json['task'] == 'Test the API'
    todo_id = response_post.json['id']

    # Get all todos
    response_get_all = client.get('/todos')
    assert response_get_all.status_code == 200
    assert len(response_get_all.json) == 1
    assert response_get_all.json[0]['task'] == 'Test the API'

    # Get specific todo
    response_get_one = client.get(f'/todos/{todo_id}')
    assert response_get_one.status_code == 200
    assert response_get_one.json['task'] == 'Test the API'

def test_update_todo(client):
    # Add a todo first
    response_post = client.post('/todos', json={'task': 'Initial Task'})
    assert response_post.status_code == 201
    todo_id = response_post.json['id']

    # Update the todo
    response_put = client.put(f'/todos/{todo_id}', json={'task': 'Updated Task', 'completed': True})
    assert response_put.status_code == 200
    assert response_put.json['task'] == 'Updated Task'
    assert response_put.json['completed'] is True

    # Verify the update
    response_get = client.get(f'/todos/{todo_id}')
    assert response_get.json['task'] == 'Updated Task'
    assert response_get.json['completed'] is True

def test_delete_todo(client):
    # Add a todo
    response_post = client.post('/todos', json={'task': 'Task to delete'})
    assert response_post.status_code == 201
    todo_id = response_post.json['id']

    # Delete the todo
    response_delete = client.delete(f'/todos/{todo_id}')
    assert response_delete.status_code == 200
    assert b"Todo deleted" in response_delete.data

    # Verify it's deleted
    response_get = client.get(f'/todos/{todo_id}')
    assert response_get.status_code == 404

def test_add_todo_no_task(client):
    response = client.post('/todos', json={})
    assert response.status_code == 400
    assert b"Task is required" in response.data

def test_get_nonexistent_todo(client):
    response = client.get('/todos/999')
    assert response.status_code == 404

def test_update_nonexistent_todo(client):
    response = client.put('/todos/999', json={'task': 'Does not matter'})
    assert response.status_code == 404

def test_delete_nonexistent_todo(client):
    response = client.delete('/todos/999')
    assert response.status_code == 404