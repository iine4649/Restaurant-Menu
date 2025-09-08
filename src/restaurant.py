# TODO: Define `MenuItem` dataclass (will be moved to menu_item.py if separated):
# - Fields: id (str), name (str), category (str), price (float), available (bool)
# - Provide `to_dict()` and `from_dict()` helpers for JSON serialization

# TODO: Implement `Restaurant` class:
# - Manage in-memory collection of MenuItem objects
# - Load from and save to `data/restaurant_data.json`
# - CRUD operations: view_all, find_by_id, find_by_name, find_by_category,
#   add_item, update_item, delete_item
# - Enforce validation via utils (unique id, proper types/ranges)

# TODO: Sorting utilities inside Restaurant:
# - sort_by_name(order="asc"|"desc")
# - sort_by_price(order="asc"|"desc")
# - sort_by_availability(available_first=True)

# TODO: Export functions:
# - export_to_csv(items, fields, path)
# - export_to_txt(items, fields, path)
# - Accept subsets (e.g., search results) and allow field selection

# TODO: Undo/History (optional):
# - Keep a stack of actions (add/update/delete) with before/after snapshots
# - Provide `undo_last_action()` that rolls back state safely

# TODO: Statistics (optional):
# - average_price_by_category()
# - count_by_category()

# TODO: Error handling strategy:
# - Raise clear custom exceptions or return error objects for invalid operations
# - Never silently fail; surface messages for UI layer


