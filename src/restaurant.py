
import json
import csv
import random


class Restaurant: 
    # TODO: Implement `Restaurant` class:
# - Manage in-memory collection of MenuItem objects
# - Load from and save to `data/restaurant_data.json`
# - CRUD operations: view_all, find_by_id, find_by_name, find_by_category,
#   add_item, update_item, delete_item
# - Enforce validation via utils (unique id, proper types/ranges)
    
    def __init__(self):
        self.menu_items = []
        self.load_data()
    
    def load_data(self):
        """Load menu items from JSON file"""
        try:
            import utils
            data = utils.load_json("data/restaurant_data.json")
            
            if data and isinstance(data, dict) and "menu" in data:
                from menu_item import MenuItem
                self.menu_items = []
                for category in data["menu"]:
                    if "items" in category:
                        for item in category["items"]:
                            # Add category information to the item
                            item["category"] = category["category"]
                            self.menu_items.append(MenuItem.from_dict(item))
                print(f"Loaded {len(self.menu_items)} menu items")
            else:
                print("No valid data found in JSON file")
                self.menu_items = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.menu_items = []
    
    def view_all(self):
        return self.menu_items


    def find_by_id(self, item_id):
        # Assumes self.menu_items is a list of MenuItem objects
        for item in getattr(self, 'menu_items', []):
            if hasattr(item, 'id') and item.id == item_id:
                return item
        return None
    
    def find_by_name(self, name):
        results = []
        for item in getattr(self, 'menu_items', []):
            if hasattr(item, 'name') and name.lower() in item.name.lower():
                results.append(item)
        return results
    
    def find_by_category(self, category):
        # Assumes self.menu_items is a list of MenuItem objects
        results = []
        for item in getattr(self, 'menu_items', []):
            if hasattr(item, 'category') and category.lower() in item.category.lower():
                results.append(item)
        return results

    def add_item(self, item):
        # Add a MenuItem object to the restaurant
        if not hasattr(self, 'menu_items'):
            self.menu_items = []
        # Check for unique id
        for existing_item in self.menu_items:
            if hasattr(existing_item, 'id') and existing_item.id == item.id:
                raise ValueError(f"ID {item.id} already exists.")
        self.menu_items.append(item)
        print("Item added.")
    
        
    def update_item(self, item_id, name=None, category=None, price=None, in_stock=None):
        # Update an existing item by ID
        item = self.find_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found.")
        
        if name is not None:
            item.name = name
        if category is not None:
            item.category = category
        if price is not None:
            item.price = price
        if in_stock is not None:
            item.in_stock = in_stock
        
        print("Item updated.") 

    def delete_item(self, item_id):
        # Delete an item by ID
        if not hasattr(self, 'menu_items'):
            self.menu_items = []
        
        for i, item in enumerate(self.menu_items):
            if hasattr(item, 'id') and item.id == item_id:
                del self.menu_items[i]
                print(f"Item with ID {item_id} deleted.")
                return
        
        raise ValueError(f"Item with ID {item_id} not found.")
# TODO: Sorting utilities inside Restaurant:
# - sort_by_name(order="asc"|"desc")
    def sort_by_name(self, order="asc"):
        reverse = True if order == "desc" else False
        try:
            if not hasattr(self, 'menu_items'):
                self.menu_items = []
            self.menu_items.sort(key=lambda item: item.name.lower(), reverse=reverse)
            print(f"Sorted Menu {'Reversed' if reverse else 'Ascended'}")
            return self.menu_items
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def sort_by_price(self, order="asc"):
        reverse = True if order == "desc" else False
        try:
            if not hasattr(self, 'menu_items'):
                self.menu_items = []
            self.menu_items.sort(key=lambda item: getattr(item, 'price', 0), reverse=reverse)
            return self.menu_items
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def sort_by_availability(self, available_first=True):
        try:
            if not hasattr(self, 'menu_items'):
                self.menu_items = []
            self.menu_items.sort(key=lambda item: not getattr(item, 'in_stock', False) if available_first else getattr(item, 'in_stock', False))
            return self.menu_items
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_data(self):
        # Return data for saving to JSON in the original format
        if not hasattr(self, 'menu_items'):
            self.menu_items = []
        
        # Group items by category
        categories = {}
        for item in self.menu_items:
            category = item.category
            if category not in categories:
                categories[category] = []
            categories[category].append(item.to_dict())
        
        # Convert to the original JSON structure
        menu = []
        for i, (category_name, items) in enumerate(categories.items(), 1):
            menu.append({
                "category": category_name,
                "id": i,
                "items": items
            })
        
        return {
            "name": "Kev's Kurry",
            "location": "45 River St, Springfield", 
            "cuisine": "Thai",
            "menu": menu
        }
        

# TODO: Undo/History (optional):
# - Keep a stack of actions (add/update/delete) with before/after snapshots
# - Provide `undo_last_action()` that rolls back state safely

