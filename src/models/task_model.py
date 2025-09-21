from os import curdir
import sqlite3
from config.config import DATABASE
from datetime import datetime

class Task:
    def __init__(self, id=None, title=None, description=None, created_at=None,
                 due_date=None, completed_at=None, status='pending',
                 priority=2, tags=None):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.due_date = due_date
        self.completed_at = completed_at
        self.status = status
        self.priority = priority
        self.tags = tags

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create_table(cls):
        with cls.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    due_date DATETIME,
                    completed_at DATETIME,
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 2,
                    tags TEXT
                )
            """)
            conn.commit()

    def save(self):
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO tasks (title, description, created_at, due_date, completed_at, status, priority, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.title, self.description, self.created_at, self.due_date,
                  self.completed_at, self.status, self.priority, self.tags))
            conn.commit()
            

    @classmethod
    def all(cls):
        with cls.get_connection() as conn:
            rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
            return [cls(**dict(row)) for row in rows]

    @classmethod
    def find(cls, task_id):
        with cls.get_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return cls(**dict(row)) if row else None

    def update(self):
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE tasks
                SET title=?, description=?, due_date=?, completed_at=?, status=?, priority=?, tags=?
                WHERE id=?
            """, (self.title, self.description, self.due_date, self.completed_at,
                  self.status, self.priority, self.tags, self.id))
            conn.commit()

    @classmethod
    def delete(cls, task_id):
        with cls.get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()