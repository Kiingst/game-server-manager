import sqlite3
from pathlib import Path

class ServerDB:
    def __init__(self, path="server_database.db"):
        self.path = Path(path)
        self._init_db()

    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._conn() as conn:
            conn.execute(""" CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                game TEXT NOT NULL,
                jar_path TEXT ,
                jvm_arguments TEXT,
                server_properties TEXT)""")

    def save_server(self, uuid, name, game, jar_path, jvm_arguments, server_properties):
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO servers (uuid, name, game, jar_path, jvm_arguments, server_properties)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(uuid) DO UPDATE SET
                    name = excluded.name,
                    game = excluded.game,
                    jar_path = excluded.jar_path,
                    jvm_arguments = excluded.jvm_arguments,
                    server_properties = excluded.server_properties
            """, (uuid, name, game, jar_path, jvm_arguments, server_properties))

    def get_server(self, uuid):
        with self._conn() as conn:
            cur = conn.execute("SELECT * FROM servers WHERE uuid = ?", (uuid,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_all_servers(self):
        with self._conn() as conn:
            cur = conn.execute("SELECT * FROM servers ORDER BY id")
            return [dict(r) for r in cur.fetchall()]

    def delete_server(self, uuid):
        with self._conn() as conn:
            conn.execute("DELETE FROM servers WHERE uuid = ?", (uuid,))                           