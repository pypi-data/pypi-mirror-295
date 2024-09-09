from typing import List


class CustomModel:
    def __init__(self, id: str, name: str, entities: List[str]):
        self.id = id
        self.name = name
        self.entities = entities

    def describe(self) -> str:
        description = f"Model Name: {self.name}\n"
        description += f"Model Id: {self.id}\n"
        description += f"Entities: {', '.join(self.entities)}\n"
        return description
