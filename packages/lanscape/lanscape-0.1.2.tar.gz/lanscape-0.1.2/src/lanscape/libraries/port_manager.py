import json
import os
from typing import List
from pathlib import Path
import importlib.resources as pkg_resources

PORT_DIR = 'lanscape.resources.ports'

class PortManager:
    def __init__(self):
        Path(PORT_DIR).mkdir(parents=True, exist_ok=True)

        self.port_lists = self.get_port_lists()

    def get_port_lists(self) -> List[str]:
        json_files = []
        
        package_dir = pkg_resources.files(PORT_DIR)
        
        if hasattr(package_dir, 'iterdir'):
            # Traverse directory and collect JSON files
            for item in package_dir.iterdir():
                if item.is_file() and item.suffix == '.json':
                    json_files.append(item.stem)
        else:
            raise RuntimeError(f"{PORT_DIR} is not a valid directory or cannot be accessed")
        
        return json_files
    
    def get_port_list(self, port_list: str) -> dict:
        if port_list not in self.port_lists: raise ValueError(f"Port list '{port_list}' does not exist. Available port lists: {self.port_lists}")

        
        data = json.load(pkg_resources.open_text(PORT_DIR, f'{port_list}.json'))

        return data if self.validate_port_data(data) else None
        
    def create_port_list(self, port_list: str, data: dict) -> bool:
        if port_list in self.port_lists: return False
        if not self.validate_port_data(data): return False

        with open(f'{PORT_DIR}{port_list}.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        self.port_lists = self.get_port_lists()
        return True
    
    def update_port_list(self, port_list: str, data: dict) -> bool:
        if port_list not in self.port_lists: return False
        if not self.validate_port_data(data): return False

        with open(f'{PORT_DIR}{port_list}.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    def delete_port_list(self, port_list: str) -> bool:
        if port_list not in self.port_lists: return False

        os.remove(f'{PORT_DIR}{port_list}.json')
        self.port_lists = self.get_port_lists()
        return True

    def validate_port_data(self, port_data: dict) -> bool:
        try:
            for port, service in port_data.items():
                port = int(port) # throws if not int
                if not isinstance(service, str): return False

                if not 0 <= port <= 65535: return False
            return True
        except:
            return False
        
