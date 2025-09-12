
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
    def view_all(self):
        if not hasattr(self, "items"):
            self.items = []
        return self.items


    def find_by_id(self, item_id):
        # Assumes self.menu_items is a list of MenuItem objects
        for item in getattr(self, 'menu_items', []):
            if hasattr(item, 'id') and item.id == item_id:
                return item
        return None
    
    def find_by_name(self, name):
       for item in getattr(self, 'menu_items', []):
            if hasattr(item, 'name') and name.lower() in item.name.lower():
                return item
       return None
    
    def find_by_category(self, category):
        # Assumes self.menu_items is a list of MenuItem objects
        results = []
        for item in getattr(self, 'menu_items', []):
            if hasattr(item, 'category') and category.lower() in item.category.lower():
                results.append(item)
        return results

    def add_item(self):
        # Prompt user for new item details and add to menu_items
        item_id = input("Enter new item ID: ").strip()
        name = input("Enter item name: ").strip()
        category = input("Enter item category: ").strip()
        # Import MenuItem if not already imported
        try:
            from menu_item import MenuItem
        except ImportError:
            print("MenuItem class not found.")
            return
        if not hasattr(self, 'menu_items'):
            self.menu_items = []
        # Check for unique id
        for item in self.menu_items:
            if hasattr(item, 'id') and item.id == item_id:
                print("ID already exists.")
                return
        new_item = MenuItem(id=item_id, name=name, category=category)
        self.menu_items.append(new_item)
        print("Item added.")
    
        
    def update_item(self):
        changing_item = input("How do you want to choose your item? id or name ").strip()
        if changing_item.lower() == 'id':
            item_id = input("Enter the ID of the item to update: ").strip()
            item = self.find_by_id(item_id)
        elif changing_item.lower() == 'name':
            name = input("Enter the name of the item to update: ").strip()
            item = self.find_by_name(name)
        else:
            print("Invalid choice.")
            return
        if not item:
            print("Item not found.")
            return
        print("What do you want to update? (id, name, category)")
        field = input("Field to update: ").strip().lower()
        if field == 'id':
            new_id = input("Enter new ID: ").strip()
            item.id = new_id
        elif field == 'name':
            new_name = input("Enter new name: ").strip()
            item.name = new_name
        elif field == 'category':
            new_category = input("Enter new category: ").strip()
            item.category = new_category
        else:
            print("Invalid field.")
            return
        print("Item updated.") 

    def delete_item(self):
        deleting_item = input("How do you want to choose your item? id or name ").strip()
        if deleting_item.lower() == 'id':
            item_id = input("Enter the ID of the item to delete: ").strip()
            item = self.find_by_id(item_id)
            ays = input(f"Are you sure you want to delete {item.name}? (y/n) ").strip().lower()
            if ays == 'y':
                del item
            elif ays == 'n':
                print("Deletion cancelled.")
                return
            else:
                print("Invalid choice.")
                return
        elif deleting_item.lower() == 'name':
            name = input("Enter the name of the item to delete: ").strip()
            item = self.find_by_name(name)
            ays = input(f"Are you sure you want to delete {item.name}? (y/n) ").strip().lower()
            if ays == 'y':
                del item
            elif ays == 'n':
                print("Deletion cancelled.")
                return
            else:
                print("Invalid choice.")
                return
        else:
            print("Invalid choice.")
            return
        if not item:
            print("Item not found.")
            return
# TODO: Sorting utilities inside Restaurant:
# - sort_by_name(order="asc"|"desc")
    def sort_by_name(self, order="asc"):
        reverse = True if order == "desc" else False
        try:
            self.menu_items.sort(key=lambda item: item.name.lower(), reverse=reverse)
            print(f"Sorted Menu {'Reversed' if reverse else 'Ascended'}")
        except Exception as e:
            print(f"Error: {e}")
# - sort_by_price(order="asc"|"desc")
    def sort_by_price(self, order="asc"):
        reverse = True if order == "desc" else False
        try: 
            self.menu_items.sort(key=lambda item: item.price.lower(), reverse=reverse)
        except Exception as e:
            print(f"Error: {e}")
# - sort_by_availability(available_first=True)
    def sort_by_availability(self,available_first = True):
        self.item.in_stock
        

# TODO: Undo/History (optional):
# - Keep a stack of actions (add/update/delete) with before/after snapshots
# - Provide `undo_last_action()` that rolls back state safely

