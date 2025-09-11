import restaurant
import utils
import menu_item
import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
import os
import time



# --- Tkinter GUI Entry Point ---
def gui_main_menu():
    rest = restaurant.Restaurant()
    root = tk.Tk()
    root.title("Restaurant Menu")

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        items = rest.view_all()
        if items:
            for item in items:
                tree.insert("", "end", values=(getattr(item, 'id', ''), getattr(item, 'name', ''), getattr(item, 'category', ''), getattr(item, 'price', ''), getattr(item, 'in_stock', '')))

    def add_item():
        try:
            item_id = entry_id.get().strip()
            name = entry_name.get().strip()
            category = entry_category.get().strip()
            price = entry_price.get().strip()
            in_stock = var_in_stock.get()
            item = menu_item.MenuItem(
                id=item_id,
                name=name,
                category=category,
                price=float(price),
                in_stock=in_stock
            )
            rest.add_item(item)
            refresh_table()
            messagebox.showinfo("Success", "Item added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No item selected.")
            return
        item_id = tree.item(selected[0])['values'][0]
        try:
            rest.delete_item(item_id)
            refresh_table()
            messagebox.showinfo("Success", "Item deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No item selected.")
            return
        item_id = tree.item(selected[0])['values'][0]
        name = entry_name.get().strip()
        category = entry_category.get().strip()
        price = entry_price.get().strip()
        in_stock = var_in_stock.get()
        try:
            rest.update_item(id=item_id, name=name, category=category, price=float(price), in_stock=in_stock)
            refresh_table()
            messagebox.showinfo("Success", "Item updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10)

    ttk.Label(frame, text="ID:").grid(row=0, column=0)
    entry_id = ttk.Entry(frame)
    entry_id.grid(row=0, column=1)

    ttk.Label(frame, text="Name:").grid(row=1, column=0)
    entry_name = ttk.Entry(frame)
    entry_name.grid(row=1, column=1)

    ttk.Label(frame, text="Category:").grid(row=2, column=0)
    entry_category = ttk.Entry(frame)
    entry_category.grid(row=2, column=1)

    ttk.Label(frame, text="Price:").grid(row=3, column=0)
    entry_price = ttk.Entry(frame)
    entry_price.grid(row=3, column=1)

    var_in_stock = tk.BooleanVar()
    ttk.Checkbutton(frame, text="In Stock", variable=var_in_stock).grid(row=4, column=1)

    ttk.Button(frame, text="Add Item", command=add_item).grid(row=5, column=0)
    ttk.Button(frame, text="Update Item", command=update_item).grid(row=5, column=1)
    ttk.Button(frame, text="Delete Item", command=delete_item).grid(row=5, column=2)

    tree = ttk.Treeview(root, columns=("ID", "Name", "Category", "Price", "In Stock"), show="headings")
    for col in ("ID", "Name", "Category", "Price", "In Stock"):
        tree.heading(col, text=col)
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    refresh_table()
    root.mainloop()

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



# TODO: Add `if __name__ == "__main__":` guard and call `main()` once implemented
if __name__ == "__main__":
    main() 





# TODO: Implement Submenus / Nested flows:
# - Search submenu: by ID, by Name (supports partial), by Category (supports partial)
# - View submenu: View All, View by Category, View by Price Range
# - Update submenu for a selected item: update name, category, price, availability
# - Sort submenu: by Name (A–Z, Z–A), by Price (low→high, high→low), by Availability

# TODO: Integrate input validation helpers from `utils.py`:
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
# - Implement undo of last action (delegates to Restaurant)




