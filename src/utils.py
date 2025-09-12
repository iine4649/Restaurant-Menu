import json
import os
import csv
import tempfile

path = "restaurant_data.json"
# TODO: Input validation helpers:
# - validate_unique_id(existing_ids, new_id) -> bool / raise ValueError
def validate_unique_id(existing_ids, new_id):
    if new_id in existing_ids:
        raise ValueError(f"ID {new_id} exists already. Please assign different ID")
    return True

# - validate_non_empty_string(value, field_name) -> str
def validate_non_empty_string(value, field_name) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value.strip()


# - validate_price(value) -> float (>= 0)
def validate_price(value) -> float:
    try:
        price = float(value)
    except (TypeError, ValueError):
        raise ValueError("Please enter price in number")
    if price < 0:
        raise ValueError("Price must be over 0")
    return price


# TODO: Formatting helpers:
# - format_items_table(items) -> str (render a simple table for CLI)
def format_items_table(items):
    if not items:
        return "Data does not exist"

    # dict
    rows = []
    for item in items:
        if hasattr(item, 'to_dict'):
            rows.append(item.to_dict())
        else:
            rows.append(dict(item))
    headers = list(rows[0].keys())
    col_widths = []
    for h in headers:
        max_len = max(len(str(row.get(h, ""))) for row in rows)
        col_widths.append(max(len(h), max_len))

    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    sep_line = "-+-".join("-" * w for w in col_widths)


    data_lines = []
    for row in rows:
        line = " | ".join(str(row.get(h, "")).ljust(w) for h, w in zip(headers, col_widths))
        data_lines.append(line)


    table = "\n".join([header_line, sep_line] + data_lines)
    return table


# - format_menu_item(item) -> str (single-line summary)

# TODO: Persistence helpers:
# - load_json(path) -> dict/list with error handling
def load_json(path):
    """Load saved user data"""
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Data loading error: {e}")
        return {}
        
# - save_json(path, data) -> None with atomic write (tmp file + replace)
def save_json(path, data):
    try:
        dir_name = os.path.dirname(path) or "."
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tmpfile:
            json.dump(data, tmpfile, ensure_ascii=False, indent=2)
            tmpfile.flush()
            os.fsync(tmpfile.fileno())
            tempname = tmpfile.name
        os.replace(tempname, path)
    except Exception as e:
        print(f"Data saving error: {e}")


# TODO: Export helpers:
# - export_to_csv(items, fields, path)
def export_to_csv(items, fields, path):
    try:
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                for item in items:
                    if hasattr(item, 'to_dict'):
                        row = item.to_dict()
                    else:
                        row = dict(item)
                    filtered_row = {field: row.get(field, "") for field in fields}
                    writer.writerow(filtered_row)
        print(f"Successfully exported CSV file: {path}")

    except Exception as e:
        print(f"Failed to export CSV file: {e}")

# - export_to_txt(items, fields, path)
def export_to_txt(items,fields,path):
    try:
        with open(path, 'w', newline='',encoding='utf-8') as txt:
            writer = txt.DicWriter(txt,fieldnames=fields)
            writer.writeheader()
            for item in items:
                if hasattr(item,'to_dict'):
                    row = item.to_dict()
                else: 
                    row = dict(item)
                filtered_row = {field: row.get(field, "") for field in fields}
                writer.writerow(filtered_row)
        print(f"Successfully exported txt file: {path}")

    except Exception as e:
        print(f"Failed to export txt file: {e}")

# TODO: Search helpers (optional):
# - normalize(text) to support partial/case-insensitive matching
def normalize(text) -> str:
    return text.title()

# - matches_partial(haystack, needle) -> bool
def matches_partial(haystack, needle) -> bool:
    if haystack in needle:
        return True
    else:
        return False

# TODO: Logging helper (optional):
# - append_action_log(path, action, before, after, timestamp)
def append_action_log(path, action, before, after, timestamp):
    try:
        with open(path, "a", encoding="utf-8") as f:
            log_entry = {
                "timestamp": timestamp,
                "action": action,
                "before": before,
                "after": after
            }
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Failed to make action log: {e}")


