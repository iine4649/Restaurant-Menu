import restaurant
import utils
import menu_item
import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QComboBox, QFileDialog, QListWidget, QInputDialog, QTextEdit  # pyright: ignore[reportMissingImports]
from PySide6.QtCore import Qt  # pyright: ignore[reportMissingImports]
import json
import datetime
import os
import time
        
from menu_item import MenuItem

path = "data/restaurant_data.json"





class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Menu Manager")
        self.restaurant = restaurant.Restaurant()
        self.resize(1000, 700)
        self.init_ui()

    def init_ui(self):
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout()
        container.setLayout(layout)

        welcome_label = QLabel("Welcome to Ethan and Shun's restaurant!")
        welcome_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(welcome_label)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addLayout(btn_layout)
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
        

    def show_menu(self):
        # [Collaborator Note] Displays all menu items in a table view.
        # Clears the main window and adds a 'Return to Home' button at the top.
        # Loads menu items from the Restaurant instance and populates the table.
        # Remove all widgets from the central widget
        container = self.centralWidget()
        for i in reversed(range(container.layout().count())):
            item = container.layout().itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                container.layout().removeItem(item)

        menu_items = self.restaurant.view_all()
        if not menu_items:
            menu_items = []
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "In Stock"])
        table.setRowCount(len(menu_items))
        
        for row, item in enumerate(menu_items):
            table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            table.setItem(row, 1, QTableWidgetItem(str(item.name)))
            table.setItem(row, 2, QTableWidgetItem(str(item.category)))
            table.setItem(row, 3, QTableWidgetItem(str(item.price)))
            table.setItem(row, 4, QTableWidgetItem("Yes" if item.in_stock else "No"))
        
        # Add sorting functionality for ID, Name, and Price
        if not hasattr(self, 'sort_orders'):
            self.sort_orders = {
                'id': 'asc',
                'name': 'asc', 
                'price': 'asc'
            }
        
        def update_table_with_items(items):
            """Helper function to update table with given items"""
            table.setRowCount(len(items))
            for row, item in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table.setItem(row, 1, QTableWidgetItem(str(item.name)))
                table.setItem(row, 2, QTableWidgetItem(str(item.category)))
                table.setItem(row, 3, QTableWidgetItem(str(item.price)))
                table.setItem(row, 4, QTableWidgetItem("Yes" if item.in_stock else "No"))
        
        def on_id_header_clicked():
            # Toggle ID sort order
            self.sort_orders['id'] = "desc" if self.sort_orders['id'] == "asc" else "asc"
            
            # Sort items by ID
            all_items = self.restaurant.view_all()
            if self.sort_orders['id'] == "asc":
                sorted_items = sorted(all_items, key=lambda x: x.id)
            else:
                sorted_items = sorted(all_items, key=lambda x: x.id, reverse=True)
            
            update_table_with_items(sorted_items)
        
        def on_name_header_clicked():
            # Toggle name sort order
            self.sort_orders['name'] = "desc" if self.sort_orders['name'] == "asc" else "asc"
            
            # Sort items by name
            sorted_items = self.restaurant.sort_by_name(self.sort_orders['name'])
            update_table_with_items(sorted_items)
        
        def on_price_header_clicked():
            # Toggle price sort order
            self.sort_orders['price'] = "desc" if self.sort_orders['price'] == "asc" else "asc"
            
            # Sort items by price
            sorted_items = self.restaurant.sort_by_price(self.sort_orders['price'])
            update_table_with_items(sorted_items)
        
        # Connect header clicks to sorting functions
        table.horizontalHeader().sectionClicked.connect(
            lambda section: (
                on_id_header_clicked() if section == 0 else
                on_name_header_clicked() if section == 1 else
                on_price_header_clicked() if section == 3 else
                None
            )
        )
        
        container.layout().addWidget(table)
        
        back_btn = QPushButton("Back to Main Menu")
        back_btn.setFixedSize(160, 40)
        container = self.centralWidget()
        container.layout().addWidget(back_btn)

        def go_back():
            
            for i in reversed(range(container.layout().count())):
                item = container.layout().itemAt(i)
                widget = item.widget()
                if widget:
                    widget.setParent(None)
                else:
                    container.layout().removeItem(item)
            
            self.init_ui()

        back_btn.clicked.connect(go_back)

    def find_item(self):
        # [Collaborator Note] Prompts the user to search for a menu item by ID, name, or category.
        # Uses Restaurant's find_by_id, find_by_name, and find_by_category methods.
        # Displays the result(s) in a message box.
        search_type, ok = QInputDialog.getItem(self, "Find Item", "Search by:", ["ID", "Name", "Category"], 0, False)
        if not ok:
            return
        value, ok = QInputDialog.getText(self, "Find Item", f"Enter {search_type}:")
        if not ok or not value:
            return
        
        result = None
        try:
            if search_type == "ID":
                item_id = int(value)
                result = self.restaurant.find_by_id(item_id)
            elif search_type == "Name":
                result = self.restaurant.find_by_name(value)
            elif search_type == "Category":
                result = self.restaurant.find_by_category(value)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid ID format. Please enter a number.")
            return
        
        if not result:
            QMessageBox.information(self, "Result", "No item found.")
        elif isinstance(result, list):
            if len(result) == 0:
                QMessageBox.information(self, "Result", "No items found.")
            else:
                items_str = "\n".join([f"ID: {item.id} - {item.name} ({item.category}) - ${item.price}" for item in result])
                QMessageBox.information(self, "Result", f"Found {len(result)} item(s):\n\n{items_str}")
        else:
            QMessageBox.information(self, "Result", f"Found item:\nID: {result.id}\nName: {result.name}\nCategory: {result.category}\nPrice: ${result.price}\nIn Stock: {'Yes' if result.in_stock else 'No'}")

    def add_item(self):
        # [Collaborator Note] Prompts the user for new item details (ID, name, category, price).
        # Creates a new MenuItem and adds it to the Restaurant instance.
        # Shows a success or error message.
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
        price, ok_price = QInputDialog.getText(self, "Add Item", "Enter item price:")
        if not ok_price or not price:
            return



        try:
            new_item = MenuItem(id=utils.validate_unique_id(self.restaurant.menu_items, int(item_id)), name=utils.normalize(name), price=utils.validate_price(price), category=utils.normalize(category))
            self.restaurant.add_item(new_item)
            QMessageBox.information(self, "Success", f"Added item: {name} in category {category} for ${price}")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input format: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add item: {e}")


    def delete_item(self):
        # [Collaborator Note] Prompts the user for an item ID to delete.
        # Calls Restaurant's delete_item method and shows a success or error message.
        item_id, ok = QInputDialog.getText(self, "Delete Item", "Enter item ID to delete:")
        if not ok or not item_id:
            return
        try:
            self.restaurant.delete_item(int(item_id))
            QMessageBox.information(self, "Success", f"Deleted item with ID: {item_id}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid ID format. Please enter a number.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete item: {e}")

    def update_item(self):
        # [Collaborator Note] Prompts the user for an item ID and new values for name, category, and price.
        # Calls Restaurant's update_item method to update the item.
        # Shows a success or error message.
        item_id, ok_id = QInputDialog.getText(self, "Update Item", "Enter item ID to update:")
        if not ok_id or not item_id:
            return
        new_name, ok_name = QInputDialog.getText(self, "Update Item", "Enter new name (leave blank to keep current):")
        new_category, ok_cat = QInputDialog.getText(self, "Update Item", "Enter new category (leave blank to keep current):")
        new_price, ok_price = QInputDialog.getText(self, "Update Item", "Enter new price (leave blank to keep current):")

        try:
            price_value = float(new_price) if new_price else None
            self.restaurant.update_item(int(item_id), name=utils.normalize(new_name) if new_name else None, category=utils.normalize(new_category) if new_category else None, price=price_value)
            QMessageBox.information(self, "Success", f"Updated item with ID: {item_id}")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input format: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update item: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

