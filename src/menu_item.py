# TODO: Define `MenuItem` dataclass (will be moved to menu_item.py if separated):
# - Fields: id (str), name (str), category (str), price (float), available (bool)
# - Provide `to_dict()` and `from_dict()` helpers for JSON serialization

from dataclasses import dataclass

@dataclass
class MenuItem:
    def __init__(self, id (str), name (str), category (str), price (float), available (bool)):
        self.id = id
        self.name = name 
        self.category = category
        self.price = price 
        self.available = available

