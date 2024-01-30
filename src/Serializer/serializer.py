import json
from abc import ABC
from pathlib import Path


class Serializer(ABC):
    def check_id_exists(self, item_id: str) -> bool:
        raise NotImplementedError


class JsonSerializer(Serializer):
    def __init__(self, json_file: Path):
        self.json_file = json_file
        print(self.json_file.absolute())

    def check_id_exists(self, item_id: str) -> bool:
        # If json doesn't exist, create, return False
        if not self.json_file.exists():
            with self.json_file.open(mode='w') as f:
                json.dump([item_id], f, indent=4)
            return False
        else:
            # Read json
            with self.json_file.open(mode='r') as f:
                id_list = json.load(f)
                print(f"before {id_list=}")
            # If item in json, return True
            if item_id in id_list:
                return True
            # If item not in json, append, return False
            else:
                id_list.append(item_id)
                print(f"after {id_list=}")
                with self.json_file.open(mode='w') as f:
                    json.dump(id_list, f, indent=4)
                return False
