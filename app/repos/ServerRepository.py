import sqlite3

from app.server_models.ServerInstance import ServerInstance

class ServerRepo:
    def __init__(self):
        
        #in init we should make sure the data base exist, if not create it
        self.db_path = "server_database.db"
        conn = sqlite3.connect(self.db_path)

        conn.cursor().execute(""" 
        CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE,
        name TEXT NOT NULL UNIQUE,
        game_id TEXT NOT NULL,
        status TEXT NOT NULL,
        path TEXT NOT NULL,
        port INTEGER NOT NULL,
        container_id TEXT,
        last_error TEXT
    );""")

        conn.commit()
        conn.close()

        



    def create(self, server: ServerInstance):

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO servers
                    (uuid, name, game_id, status, path, port, container_id, last_error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    server.uuid,
                    server.name,
                    server.game_id,
                    server.status,
                    server.path,
                    server.port,
                    server.container_id,
                    server.last_error,
                ),
            )

            server.update_server_id(cursor.lastrowid)

        return server


        

    def get(self, uuid):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM servers WHERE uuid = ?",
                (uuid,),
            )
            return cursor.fetchone()
        

    def list_all_server_uuids(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT uuid FROM servers"
            )
            return [row[0] for row in cursor.fetchall()]
            

        

    def update(self, server):
        if server.id is None:
            raise ValueError("Cannot update a server without an id")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                UPDATE servers
                SET name = ?,
                    game_id = ?,
                    status = ?,
                    path = ?,
                    port = ?,
                    container_id = ?,
                    last_error = ?
                WHERE id = ?
                """,
                (
                    server.name,
                    server.game_id,
                    server.status,
                    server.path,
                    server.port,
                    server.container_id,
                    server.last_error,
                    server.id,
                ),
            )

            return cursor.rowcount > 0

    def delete(self, uuid):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM servers WHERE uuid = ?",
                (uuid,),
            )

            return cursor.rowcount > 0