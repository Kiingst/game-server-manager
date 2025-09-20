from pathlib import Path
import os
import uuid



class Server:

    def __init__(self, name, uuids="") -> None:
        #if you dont give a UUID generate one
        if uuids == "":
            self.uuid = str(uuid.uuid4())
            print(f"set uuid to {self.uuid}")
        else:
            self.uuid = uuids

        self.name = name
        self.base_path = Path("servers") / f"{self.name}_{self.uuid}"
        self.create_server_dir()
        

    def create_server_dir(self):
        
        base_path = self.base_path
        os.makedirs(base_path, exist_ok= True)
        print(f"Created server at {base_path}")
    




