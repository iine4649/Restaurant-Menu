import restaurant
import utils
import menu_item
import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QComboBox, QFileDialog, QListWidget, QInputDialog, QTextEdit
import json
import datetime
import os
import time


# TODO: Implement CLI entry-point for the Restaurant Menu application.
# - Wire up `Restaurant` (from restaurant.py) and `MenuItem` (from menu_item.py) once created
# - Load JSON data from `data/restaurant_data.json` at startup
# - Persist changes back to JSON on-demand and on exit (confirm with user)
# --- CLI Entry Points for Restaurant Menu Application ---
path = "restaurant_data.json"



 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Menu Manager")
        container = QWidget()  
        self.setCentralWidget(container)
        layout = QVBoxLayout()
        container.setLayout(layout)

    # Horizontal layout for buttons
        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        btn_show_menu = QPushButton("Show Menu")
        btn_show_menu.setFixedSize(120, 40)
        btn_layout.addWidget(btn_show_menu)
        btn_show_menu.clicked.connect(self.show_menu)

        btn_find_item = QPushButton("Find Item")
        btn_find_item.setFixedSize(120, 40)
        btn_layout.addWidget(btn_find_item)
        btn_find_item.clicked.connect(self.find_item)

    def show_menu(self):
        QMessageBox.information(self, "Menu", "Menu would be displayed here.")

    def find_item(self):
        QMessageBox.information(self, "Find Item", "Item search functionality would be here.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

def cli_main_menu():
    """Main CLI menu loop."""
    print("Welcome to the Restaurant Menu CLI!")
    data = utils.load_json()
    if not data:
        print("Failed to load restaurant data. Exiting.")
        return

    # Instantiate Restaurant class (assumes Restaurant can be initialized with data)
    try:
        rest = restaurant.Restaurant()
        # If Restaurant class needs to load data, you may need to call a method here
    except Exception as e:
        print(f"Error initializing Restaurant: {e}")
        return

    while True:
        print("\n--- Main Menu ---")
        print("1. View All Menu Items")
        print("2. Search Menu Items")
        print("3. Add Menu Item")
        print("4. Update Menu Item")
        print("5. Delete Menu Item")
        print("6. Save Changes")
        print("7. Sort Menu Items")
        print("8. Export Menu")
        print("9. Show Statistics")
        print("0. Quit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # View all items
            items = rest.view_all()
            if items:
                print(utils.format_items_table(items))
            else:
                print("No menu items found.")
        elif choice == "2":
            print("Search by: 1) ID  2) Name  3) Category")
            sub = input("Choose search type: ").strip()
            if sub == "1":
                id_str = input("Enter item ID: ").strip()
                try:
                    item = rest.find_by_id(int(id_str))
                    if item:
                        print(utils.format_items_table([item]))
                    else:
                        print("Item not found.")
                except Exception as e:
                    print(f"Error: {e}")
            elif sub == "2":
                name = input("Enter item name (partial allowed): ").strip()
                items = rest.find_by_name(name)
                if items:
                    print(utils.format_items_table(items))
                else:
                    print("No items found.")
            elif sub == "3":
                cat = input("Enter category (partial allowed): ").strip()
                items = rest.find_by_category(cat)
                if items:
                    print(utils.format_items_table(items))
                else:
                    print("No items found.")
            else:
                print("Invalid search type.")
        elif choice == "3":
            # Add item
            try:
                name = input("Enter name: ").strip()
                price = input("Enter price: ").strip()
                category = input("Enter category: ").strip()
                in_stock = input("In stock? (y/n): ").strip().lower() == "y"
                # You may need to generate a unique ID here
                # This is a placeholder; actual implementation may differ
                new_id = int(time.time())
                item = menu_item.MenuItem(
                    id=new_id,
                    name=utils.validate_non_empty_string(name, "Name"),
                    price=utils.validate_price(price),
                    in_stock=in_stock
                )
                # Add to restaurant
                rest.add_item(item)
                print("Item added successfully.")
            except Exception as e:
                print(f"Failed to add item: {e}")
        elif choice == "4":
            # Update item
            try:
                id_str = input("Enter ID of item to update: ").strip()
                item = rest.find_by_id(int(id_str))
                if not item:
                    print("Item not found.")
                    continue
                print("Leave field blank to keep current value.")
                name = input(f"New name [{item.name}]: ").strip() or item.name
                price = input(f"New price [{item.price}]: ").strip() or item.price
                in_stock = input(f"In stock? (y/n) [{item.in_stock}]: ").strip()
                if in_stock == "":
                    in_stock = item.in_stock
                else:
                    in_stock = in_stock.lower() == "y"
                # Update item
                rest.update_item(
                    id=int(id_str),
                    name=name,
                    price=price,
                    in_stock=in_stock
                )
                print("Item updated successfully.")
            except Exception as e:
                print(f"Failed to update item: {e}")
        elif choice == "5":
            # Delete item
            try:
                id_str = input("Enter ID of item to delete: ").strip()
                rest.delete_item(int(id_str))
                print("Item deleted successfully.")
            except Exception as e:
                print(f"Failed to delete item: {e}")
        elif choice == "6":
            # Save changes
            # You may need to get data from Restaurant instance
            try:
                # This assumes Restaurant has a method to get current data
                data = rest.get_data()
                utils.save_json(path,data)
            except Exception as e:
                print(f"Failed to save: {e}")
        elif choice == "7":
            print("Sort by: 1) Name  2) Price  3) Availability")
            sub = input("Choose sort type: ").strip()
            if sub == "1":
                order = input("Order (asc/desc): ").strip().lower()
                items = rest.sort_by_name(order)
                print(utils.format_items_table(items))
            elif sub == "2":
                order = input("Order (asc/desc): ").strip().lower()
                items = rest.sort_by_price(order)
                print(utils.format_items_table(items))
            elif sub == "3":
                avail = input("Available first? (y/n): ").strip().lower() == "y"
                items = rest.sort_by_availability(avail)
                print(utils.format_items_table(items))
            else:
                print("Invalid sort type.")
        elif choice == "8":
            print("Export to: 1) CSV  2) TXT")
            sub = input("Choose export type: ").strip()
            path = input("Enter output file path: ").strip()
            fields = input("Enter fields to export (comma separated): ").strip().split(",")
            items = rest.view_all()
            if sub == "1":
                utils.export_to_csv(items, fields, path)
            elif sub == "2":
                # Placeholder for TXT export
                print("TXT export not implemented.")
            else:
                print("Invalid export type.")
        elif choice == "9":
            # Show statistics (placeholder)
            print("Statistics feature not implemented.")
        elif choice == "0":
            confirm = input("Save changes before quitting? (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    data = rest.get_data()
                    utils.save_json(path,data)
                except Exception as e:
                    print(f"Failed to save: {e}")
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

# TODO: Build Main Menu loop (robust, user-friendly):
# - Options: View, Search, Add, Update, Delete, Save, Sort, Export, Statistics, Undo, Quit
# - Validate input; re-prompt gracefully for invalid menu selections
# - Keep the UI consistent and clear
def main():
    while True:
        print("1. Boot on CLI")
        print("0. Exit")
        choice = input("Select Boot Option: ").strip()
        if choice == "1":
            cli_main_menu()
        elif choice == "0":
            print("Exiting the application...")
            break
        else:
            print("Invalid Selection")



# TODO: Add `if __name__ == "__main__":` guard and call `main()` once implemente



# - Search submenu: by ID, by Name (supports partial), by Category (supports partial)
# - View submenu: View All, View by Category, View by Price Range
# - Update submenu for a selected item: update name, category, price, availability
# - Sort submenu: b   y Name (A–Z, Z–A), by Price (low→high, high→low), by Availability
# - Sort submenu: by Name (A–Z, Z–A), by Price (low→high, high→low), by Availability


# TODO: Integrate idnput validation helpers from `utils.py`:
# - Ensure unique IDs when adding new items
# - Validate numeric fields (price >= 0 etc.)
# - Validate non-empty strings for name/category
# - Gracefully handle not-found cases with warnings


# TODO: Formatting and UX helpers:
# - Use table formatting (from utils) for listing items
# - Show clear success/error messages



# TODO: Optional enhancements:
# - Action logging (add/update/delete) to a log file
# - Show simple statistics (e.g., average price by category)

