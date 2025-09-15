
import json
import csv
import random


class Restaurant: 

    
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
                            
                            item["category"] = category["category"]
                            self.menu_items.append(MenuItem.from_dict(item))
                print(f"Loaded {len(self.menu_items)} menu items")
            else:
                print("No valid data found in JSON file")
                self.menu_items = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.menu_items = []
    
    def save_data(self):
        """Save menu items to JSON file"""
        try:
            import utils
            data = self.get_data()
            utils.save_json("data/restaurant_data.json", data)
            print("Data saved successfully")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def view_all(self):
        return self.menu_items


    def find_by_id(self, item_id):
        
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
        
        results = []
        for item in getattr(self, 'menu_items', []):
            if hasattr(item, 'category') and category.lower() in item.category.lower():
                results.append(item)
        return results

    def add_item(self, item):
        
        if not hasattr(self, 'menu_items'):
            self.menu_items = []
        
        for existing_item in self.menu_items:
            if hasattr(existing_item, 'id') and existing_item.id == item.id:
                raise ValueError(f"ID {item.id} already exists.")
        self.menu_items.append(item)
        self.save_data()
        print("Item added.")
    
        
    def update_item(self, item_id, name=None, category=None, price=None, in_stock=None):
        
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
        
        self.save_data()
        print("Item updated.") 

    def delete_item(self, item_id):
        
        if not hasattr(self, 'menu_items'):
            self.menu_items = []
        
        for i, item in enumerate(self.menu_items):
            if hasattr(item, 'id') and item.id == item_id:
                del self.menu_items[i]
                self.save_data()
                print(f"Item with ID {item_id} deleted.")
                return
        
        raise ValueError(f"Item with ID {item_id} not found.")

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
        
        if not hasattr(self, 'menu_items'):
            self.menu_items = []
        
        
        categories = {}
        for item in self.menu_items:
            category = item.category
            if category not in categories:
                categories[category] = []
            categories[category].append(item.to_dict())
        
        
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
        


