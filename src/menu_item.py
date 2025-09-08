from dataclasses import dataclass
from typing import Any, Dict


# TODO: This dataclass intentionally matches the item shape in data/restaurant_data.json
#   {"id": int, "name": str, "price": float, "in_stock": bool}
@dataclass
class MenuItem:
    id: int
    name: str
    price: float
    in_stock: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-compatible dictionary matching restaurant_data.json schema."""
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
            "in_stock": bool(self.in_stock),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MenuItem":
        """Create a MenuItem from a dict with keys id, name, price, in_stock."""
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            price=float(data["price"]),
            in_stock=bool(data.get("in_stock", True)),
        )


# Minimal helper to construct item dicts directly, if a class instance is not desired.
def make_item_dict(item_id: int, name: str, price: float, in_stock: bool = True) -> Dict[str, Any]:
    """Return a dict compatible with entries in data/restaurant_data.json -> menu[*].items[*]."""
    return {
        "id": int(item_id),
        "name": str(name),
        "price": float(price),
        "in_stock": bool(in_stock),
    }
