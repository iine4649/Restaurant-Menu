# Lab\_02 (Partners) User-Driven Applications with JSON

## **Theme**

In this lab, you and a partner will design a **menu-driven program** that interacts with a JSON dataset of restaurant data. The program should let a user view, search, add, update, and delete menu items, while maintaining a clean project structure and good documentation.

---

## Learning Goals

* Practice **collaborating with a partner** on code design and division of work
* Build a **user-driven application** using **classes** to organize code
* Manipulate and persist data stored in JSON files
* Write **modular, reusable code** split into multiple source files
* Document your work in a `README.md`
* Organize code into a proper **project folder structure**

---

## Project Structure

```bash
|restaurant_manager/
|   data/             
|       restaurant_data.json   # JSON file containing menu items
|   src/              
|       main.py               # Main program logic
|       restaurant.py         # Class for restaurant operations (view, add, delete, update)
|       utils.py              # Optional helper functions
|   assets/           
|       README.md             # Documentation, optional images or exports
|   env/                     # Virtual Environment if needed
|   requirements.txt          # Dependencies for Virtual Environment
|
|   # The env/ folder and requirements.txt will be generated automatically during setup.
```

---

## Requirements

1. **Use multiple source files**:

   * `Restaurant` class in `restaurant.py`
   * `MenuItem` class in `menu_item.py`
   * `main.py` imports and uses both
2. **Load data** from a JSON file (`restaurant_data.json`).
3. **Provide a menu** for the user to choose actions.
4. Implement at least **five different functions**:

   * View all menu items
   * Search for a menu item by key (id, name, or category)
   * Add a new menu item
   * Update an existing menu item
   * Delete a menu item
   * Save changes back to the JSON file
5. **Validate input** where possible (wrong menu choices, invalid ids).
6. Include a **README.md** document:

   * Program description
   * Setup and run instructions
   * Example input/output interaction
   * Folder structure explanation
7. **Collaborate with your partner**:

   * Divide responsibilities (one works on `Restaurant` class, the other on `MenuItem` class or menu logic for example)
   * Commit code regularly so contributions are visible
   * Perform code reviews before merging

---

## Deliverables

1. A working application in your repo with correct multi-file structure.
2. `README.md` with instructions and documentation.
3. A JSON dataset included in `data/`.
4. Evidence of **collaborative effort** (commits, shared design).

---

## Partner Collaboration Guidelines

* Switch roles: one partner “drives” (types) while the other “navigates” (reviews and suggests)
* Use GitHub to track commits and collaboration
* Plan your class design together before coding

---

## <span style="color: red;">Challenge Goals (Required Additions)</span>

* Sorting (by name, category, price, or availability)

  * Item Name (A–Z, Z–A)
  * Price (lowest → highest, highest → lowest)
  * Availability (available, out of stock)
* Input validation

  * Ensure unique IDs when adding new menu items
  * Check numeric fields (e.g., price) for valid ranges
  * Validate string fields (e.g., name and category cannot be empty)
  * Handle invalid menu choices gracefully (re-prompt user)
  * Warn the user when updating/deleting a non-existent item
* Export to CSV or text file

  * Export filtered or sorted results to CSV or plain text
  * Allow user to choose which fields to export
  * Allow export of search results only
* Submenus or nested functionality (Optional)

  * Main Menu → Search → Search by Name / Category / ID
  * Main Menu → View → View All / View by Category / View by Price
  * Implement nested editing:

    * When updating a menu item, show a submenu: update name, category, price, or availability
* Refactor helpers into `src/utils.py`

  * Input validation functions
  * Formatting functions (e.g., print tables nicely)
  * File export functions
  * Sorting helpers
* Extra Enhancements (Optional)

  * Search with partial matches (e.g., typing "Pad Thai" finds all Thai dishes)
  * Keep a history of changes (log file of add/update/delete actions)
  * Add price averages or category statistics
  * Implement undo last action

---

## RUBRIC (Standard Version)

| Category                   | Exemplary (A)                                                               | Proficient (B)                           | Developing (C)                           | Beginning (D/F)                                           |
| -------------------------- | --------------------------------------------------------------------------- | ---------------------------------------- | ---------------------------------------- | --------------------------------------------------------- |
| **Functionality (30%)**    | All required features implemented, works smoothly, data persists correctly  | Most features implemented, minor bugs    | Some features missing or buggy           | Program does not run or lacks key features                |
| **User Interaction (20%)** | Clear menu, good input validation, handles errors gracefully                | Menu works but limited validation        | Menu works but clunky or unclear         | No usable menu or very confusing                          |
| **Code Structure (20%)**   | Proper use of classes, multi-file design, modular functions                 | Classes used, some modularity issues     | Limited class usage, messy structure     | All code in main.py, no classes                           |
| **Documentation (10%)**    | README thorough: description, setup, examples, folder structure explained   | README present but missing some elements | README minimal and unclear               | No README provided                                        |
| **Collaboration (20%)**    | Evidence of strong teamwork, commits from both partners, even contributions | Both contributed but unevenly            | Minimal collaboration, one did most work | One partner did nearly all the work, little collaboration |

**Total: 100 points**

---

## RUBRIC (Challenge Version)

| Category                                    | Exemplary (A)                                                                                                                                              | Proficient (B)                                                                       | Developing (C)                                                                | Beginning (D/F)                                           |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Functionality (30%)**                     | All required features implemented: view, search, add, update, delete, save; sorting works; export functions work; data persists correctly                  | Most features implemented; minor issues with sorting or export; data mostly persists | Some features missing, buggy, or partially working; sorting/export incomplete | Program does not run or lacks key features                |
| **Input Validation & Error Handling (15%)** | Robust input validation: unique IDs, numeric fields checked, strings not empty; invalid menu choices handled gracefully; warnings for non-existent records | Input validation implemented but may miss edge cases; minor error handling issues    | Minimal validation; program may crash or behave incorrectly on invalid input  | No input validation; program crashes on invalid input     |
| **User Interaction & Menu Design (15%)**    | Clear, intuitive menu; submenus/nested options implemented; editing/addition menus well structured                                                         | Menu mostly clear; some nested functionality missing or confusing                    | Menu works but unclear or cumbersome; submenus absent or confusing            | Menu confusing or unusable; no nested functionality       |
| **Code Structure & Modularity (20%)**       | Proper use of classes; multi-file design; helpers refactored into `utils.py`; functions reusable and modular                                               | Classes used, some modularity issues; helpers may still be in main                   | Limited class usage; code mostly in main; helpers not modular                 | All code in main.py; no classes or modularity             |
| **Documentation (10%)**                     | README thorough: description, setup, examples, folder structure explained; code well-commented                                                             | README present but missing some elements; some comments                              | README minimal or unclear; few comments                                       | No README; no code comments                               |
| **Collaboration (10%)**                     | Evidence of strong teamwork; both partners contributed; commits show even work distribution                                                                | Both contributed but unevenly; minor gaps in collaboration                           | Minimal collaboration; one partner did most work                              | One partner did nearly all the work; little collaboration |

**Total: 100 points**