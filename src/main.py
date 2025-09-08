# TODO: Implement CLI entry-point for the Restaurant Menu application.
# - Wire up `Restaurant` (from restaurant.py) and `MenuItem` (from menu_item.py) once created
# - Load JSON data from `data/restaurant_data.json` at startup
# - Persist changes back to JSON on-demand and on exit (confirm with user)

# TODO: Build Main Menu loop (robust, user-friendly):
# - Options: View, Search, Add, Update, Delete, Save, Sort, Export, Statistics, Undo, Quit
# - Validate input; re-prompt gracefully for invalid menu selections
# - Keep the UI consistent and clear

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

# TODO: Export features:
# - Allow exporting current/filtered/sorted/search results to CSV or TXT
# - Let user choose which fields to export and output path

# TODO: Formatting and UX helpers:
# - Use table formatting (from utils) for listing items
# - Show clear success/error messages

# TODO: Optional enhancements:
# - Action logging (add/update/delete) to a log file
# - Show simple statistics (e.g., average price by category)
# - Implement undo of last action (delegates to Restaurant)

# TODO: Add `if __name__ == "__main__":` guard and call `main()` once implemented


