import json
import os
path = "restaurant_data.json"
# TODO: Input validation helpers:
# - validate_unique_id(existing_ids, new_id) -> bool / raise ValueError
# - validate_non_empty_string(value, field_name) -> str
# - validate_price(value) -> float (>= 0)

# TODO: Formatting helpers:
# - format_items_table(items) -> str (render a simple table for CLI)
# - format_menu_item(item) -> str (single-line summary)

# TODO: Persistence helpers:
# - load_json(path) -> dict/list with error handling
def load_json(path):
    """Load saved user data"""
    try:
        if os.path.exists(path.data_file):
            with open(path.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Data loading error: {e}")
        return {}
# - save_json(path, data) -> None with atomic write (tmp file + replace)
def save_json(path, data):
    """Save data to Json"""
    try:
        if os.path.exists(path.data_file):
            with open(path.data_file, 'w', encoding='utf-8') as f:
                json.dump(path.user_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Data saving error: {e}")
        return {}

# TODO: Export helpers:
# - export_to_csv(items, fields, path)
# - export_to_txt(items, fields, path)

# TODO: Search helpers (optional):
# - normalize(text) to support partial/case-insensitive matching
# - matches_partial(haystack, needle) -> bool

# TODO: Logging helper (optional):
# - append_action_log(path, action, before, after, timestamp)


