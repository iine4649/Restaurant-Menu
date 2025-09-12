import restaurant
import utils
import menu_item
import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QComboBox, QFileDialog, QListWidget, QInputDialog, QTextEdit
from PySide6.QtCore import Qt
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

# --- Tkinter GUI Entry Point --



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Menu Manager")
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout()
        container.setLayout(layout)

        # Add welcome label at the top
        welcome_label = QLabel("Welcome to Ethan and Shun's restaurant!")
        welcome_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(welcome_label)

        # Horizontal layout for buttons, centered below the label
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addLayout(btn_layout)

        # Add all buttons to the same horizontal layout, aligned top center
        buttons = [
            ("Show Menu", self.show_menu),
            ("Find Item", self.find_item),
            ("Add Item", self.add_item),
            ("Delete Item", self.delete_item),
            ("Update Item", self.update_item)
        ]

        for text, slot in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(120, 40)
            btn_layout.addWidget(btn)
            btn.clicked.connect(slot)

        self.restaurant = restaurant.Restaurant()

    def show_menu(self):
        # Remove all widgets from the central widget
        container = self.centralWidget()
        for i in reversed(range(container.layout().count())):
            item = container.layout().itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                container.layout().removeItem(item)

    # Load menu items from JSON
        data = utils.load_json("restaurant_data.json")
        if not data:
            data = []
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price"])
        table.setRowCount(len(data))
        for row, item in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(str(item.get("id", ""))))
            table.setItem(row, 1, QTableWidgetItem(str(item.get("name", ""))))
            table.setItem(row, 2, QTableWidgetItem(str(item.get("category", ""))))
            table.setItem(row, 3, QTableWidgetItem(str(item.get("price", ""))))
        container.layout().addWidget(table)

    def find_item(self):
        # Prompt for search type
        search_type, ok = QInputDialog.getItem(self, "Find Item", "Search by:", ["ID", "Name", "Category"], 0, False)
        if not ok:
            return
        value, ok = QInputDialog.getText(self, "Find Item", f"Enter {search_type}:")
        if not ok or not value:
            return
        result = None
        if search_type == "ID":
            result = self.restaurant.find_by_id(value)
        elif search_type == "Name":
            result = self.restaurant.find_by_name(value)
        elif search_type == "Category":
            result = self.restaurant.find_by_category(value)
        # Display result
        if not result:
            QMessageBox.information(self, "Result", "No item found.")
        elif isinstance(result, list):
            items_str = "\n".join([str(getattr(item, 'name', item)) for item in result])
            QMessageBox.information(self, "Result", f"Found items:\n{items_str}")
        else:
            QMessageBox.information(self, "Result", f"Found item: {getattr(result, 'name', result)}")

    def add_item(self):
        # Prompt for new item details
        item_id, ok_id = QInputDialog.getText(self, "Add Item", "Enter new item ID:")
        if not ok_id or not item_id:
            return
        name, ok_name = QInputDialog.getText(self, "Add Item", "Enter item name:")
        if not ok_name or not name:
            return
        category, ok_cat = QInputDialog.getText(self, "Add Item", "Enter item category:")
        if not ok_cat or not category:
            return
        # Add to restaurant
        try:
            from menu_item import MenuItem
            new_item = MenuItem(id=item_id, name=name, category=category)
            if not hasattr(self.restaurant, 'menu_items'):
                self.restaurant.menu_items = []
            self.restaurant.menu_items.append(new_item)
            QMessageBox.information(self, "Success", f"Added item: {name} in category {category}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add item: {e}")
    def delete_item(self):
        item_id, ok = QInputDialog.getText(self, "Delete Item", "Enter item ID to delete:")
        if not ok or not item_id:
            return
        try:
            self.restaurant.delete_item(item_id)
            QMessageBox.information(self, "Success", f"Deleted item with ID: {item_id}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete item: {e}")
    def update_item(self):
        item_id, ok_id = QInputDialog.getText(self, "Update Item", "Enter item ID to update:")
        if not ok_id or not item_id:
            return
        new_name, ok_name = QInputDialog.getText(self, "Update Item", "Enter new name (leave blank to keep current):")
        new_category, ok_cat = QInputDialog.getText(self, "Update Item", "Enter new category (leave blank to keep current):")
        try:
            self.restaurant.update_item(item_id, name=new_name if new_name else None, category=new_category if new_category else None)
            QMessageBox.information(self, "Success", f"Updated item with ID: {item_id}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update item: {e}")
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




@@ -249,19 +24,17 @@ def main():
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

