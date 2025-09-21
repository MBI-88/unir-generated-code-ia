from unittest.mock import patch, MagicMock, call
from src.models.task_model import Task


def make_conn_mock(
    *,
    insert_lastrowid=None,
    select_one_row=None,
    select_all_rows=None
):
    """
    Crea un mock de conexión SQLite que soporta 'with' y emula execute().fetch*().
    Puedes parametrizar:
      - insert_lastrowid: id a devolver tras INSERT.
      - select_one_row: dict (o None) para .fetchone().
      - select_all_rows: lista de dicts para .fetchall().
    """
    conn = MagicMock()
    conn.__enter__.return_value = conn  # para soportar "with"

    # Cursors por tipo de operación
    insert_cursor = MagicMock()
    if insert_lastrowid is not None:
        insert_cursor.lastrowid = insert_lastrowid

    select_one_cursor = MagicMock()
    select_one_cursor.fetchone.return_value = select_one_row

    select_all_cursor = MagicMock()
    select_all_cursor.fetchall.return_value = select_all_rows or []

    update_cursor = MagicMock()
    delete_cursor = MagicMock()
    create_table_cursor = MagicMock()

    def execute_side_effect(sql, *params):
        sql_up = sql.strip().upper()
        if sql_up.startswith("CREATE TABLE"):
            return create_table_cursor
        if sql_up.startswith("INSERT"):
            return insert_cursor
        if sql_up.startswith("UPDATE"):
            return update_cursor
        if sql_up.startswith("DELETE"):
            return delete_cursor
        if sql_up.startswith("SELECT"):
            # Heurística simple para diferenciar SELECTs
            if "WHERE ID =" in sql_up:
                return select_one_cursor
            return select_all_cursor
        # fallback
        return MagicMock()

    conn.execute.side_effect = execute_side_effect
    return conn


from unittest.mock import patch, MagicMock
from src.models.task_model import Task

def test_create_and_find_task_with_mock():
    # Creamos un cursor simulado con lastrowid
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 1
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "title": "Mock Task",
        "description": "Testing with mock",
        "created_at": "2025-09-21 12:00:00",
        "due_date": None,
        "completed_at": None,
        "status": "pending",
        "priority": 2,
        "tags": None,
    }

    # Creamos la conexión simulada que soporta "with"
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.execute.return_value = mock_cursor

    # Parchamos Task.get_connection para que devuelva nuestro mock
    with patch.object(Task, "get_connection", return_value=mock_conn):
        task = Task(id=1, title="Mock Task", description="Testing with mock")
        task.save()
        assert task.id == 1 

        found = Task.find(1)
        assert found is not None
        assert found.title == "Mock Task"


def test_update_task_with_mock():
    # Mock de conexión que soporte UPDATE
    conn = make_conn_mock()
    with patch.object(Task, "get_connection", return_value=conn):
        task = Task(id=42, title="Old Title", description="desc")
        task.title = "Updated Title"
        task.update()

        # Aseguramos que se llamó a UPDATE con los parámetros esperados
        assert conn.execute.call_count >= 1
        update_calls = [c for c in conn.execute.call_args_list if "UPDATE tasks" in c.args[0]]
        assert len(update_calls) == 1
        sql, params = update_calls[0].args[0], update_calls[0].args[1]
        # params = (title, description, due_date, completed_at, status, priority, tags, id)
        assert params[-1] == 42
        assert params[0] == "Updated Title"


def test_delete_task_with_mock():
    # Primero simulamos el DELETE
    conn_delete = make_conn_mock()
    with patch.object(Task, "get_connection", return_value=conn_delete):
        Task.delete(7)
        # Verificamos que hubo un DELETE con el id correcto
        delete_calls = [c for c in conn_delete.execute.call_args_list if "DELETE FROM tasks" in c.args[0]]
        assert len(delete_calls) == 1
        _, params = delete_calls[0].args[0], delete_calls[0].args[1]
        assert params == (7,)

    # Luego, simulamos que el SELECT posterior no encuentra la fila
    conn_find_none = make_conn_mock(select_one_row=None)
    with patch.object(Task, "get_connection", return_value=conn_find_none):
        deleted = Task.find(7)
        assert deleted is None


def test_all_tasks_with_mock():
    # Simulamos un SELECT * con dos filas
    rows = [
        {
            "id": 1,
            "title": "Task 1",
            "description": None,
            "created_at": "2025-09-21 10:00:00",
            "due_date": None,
            "completed_at": None,
            "status": "pending",
            "priority": 2,
            "tags": None,
        },
        {
            "id": 2,
            "title": "Task 2",
            "description": None,
            "created_at": "2025-09-21 11:00:00",
            "due_date": None,
            "completed_at": None,
            "status": "in_progress",
            "priority": 1,
            "tags": "work,urgent",
        },
    ]
    conn = make_conn_mock(select_all_rows=rows)

    with patch.object(Task, "get_connection", return_value=conn):
        tasks = Task.all()
        assert len(tasks) == 2
        titles = [t.title for t in tasks]
        assert "Task 1" in titles and "Task 2" in titles