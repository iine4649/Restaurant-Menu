# TODO: Input validation helpers:
# - validate_unique_id(existing_ids, new_id) -> bool / raise ValueError
# - validate_non_empty_string(value, field_name) -> str
# - validate_price(value) -> float (>= 0)

# TODO: Formatting helpers:
# - format_items_table(items) -> str (render a simple table for CLI)
# - format_menu_item(item) -> str (single-line summary)

# TODO: Persistence helpers:
# - load_json(path) -> dict/list with error handling
# - save_json(path, data) -> None with atomic write (tmp file + replace)

# TODO: Export helpers:
# - export_to_csv(items, fields, path)
# - export_to_txt(items, fields, path)

# TODO: Search helpers (optional):
# - normalize(text) to support partial/case-insensitive matching
# - matches_partial(haystack, needle) -> bool

# TODO: Logging helper (optional):
# - append_action_log(path, action, before, after, timestamp)


