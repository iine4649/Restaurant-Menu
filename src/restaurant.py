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
        return None

    def find_by_id(self):
        return None
    
    def find_by_name(self):
        return None
    
    def find_by_category(self):
        return None

    def add_item(self):
    
        try:
            name = self.name_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter the name of food")
                return
            
            
            # User Info
            user_info = {
                "name": name,

            }
            
            
            # Save data
            self.user_data[name] = user_info
            self.save_user_data()
            
            # Display results
            self.display_results(user_info)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_item():
        return None

    def delete_item():
        return None
# TODO: Sorting utilities inside Restaurant:
# - sort_by_name(order="asc"|"desc")
# - sort_by_price(order="asc"|"desc")
# - sort_by_availability(available_first=True)
    def sort_by_name(bool AscOrDesc):
        return None
    


# TODO: Export functions:
# - export_to_csv(items, fields, path)
# - export_to_txt(items, fields, path)
# - Accept subsets (e.g., search results) and allow field selection
    def export_to_csv(items, fields, path):
        return None
    def export_to_txt(items,fields,path):

# TODO: Undo/History (optional):
# - Keep a stack of actions (add/update/delete) with before/after snapshots
# - Provide `undo_last_action()` that rolls back state safely

# TODO: Statistics (optional):
# - average_price_by_category()
# - count_by_category()

# TODO: Error handling strategy:
# - Raise clear custom exceptions or return error objects for invalid operations
# - Never silently fail; surface messages for UI layer


