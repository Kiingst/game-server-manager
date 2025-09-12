from pathlib import Path
import os
import UUID



class Server:

    def __init__(self, name, uuid="") -> None:

        #if you give a UUID generate one
        if uuid == "":
            self.UUID = str(UUID.uuid4())
        else
            self.UUID = uuid

        self.name = name
        self.base_path = Path("servers") / f"{self.name}_{self.UUID}"
        self.create_server_dir()
        

    def create_server_dir(self):
        
        base_path = self.base_path
        os.makedirs(base_path, exist_ok= True)
        print(f"Created server at {base_path}")
    




