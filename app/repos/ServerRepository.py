import sqlite3

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

        



    def create(self, server):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO servers
                    (name, game_id, status, path, port, container_id, last_error)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
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


        

    def get(self, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM servers WHERE id = ?",
                (server_id,),
            )
            return cursor.fetchone()
        

    def list_all(self):
        pass
        #list all servers in data base return a json list

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

    def delete(self, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM servers WHERE id = ?",
                (server_id,),
            )

            return cursor.rowcount > 0