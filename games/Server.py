from pathlib import Path
import os




class Server:

    def __init__(self, name, game) -> None:
        self.name = name
        self.game = game
        self.base_path = Path("servers") / game / name
        self.process = None
        

    def create_server_dir(self):
        
        base_path = self.base_path
        os.makedirs(base_path, exist_ok= True)
        with open(base_path / "eula.txt", "w") as eula:
            eula.write("eula=true\n")

        print(f"Created server at {base_path}")
    




