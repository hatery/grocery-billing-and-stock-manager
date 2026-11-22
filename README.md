# Grocery Billing and Stock Manager

A menu-driven Python application for managing a small grocery shop. It maintains item stock, creates customer bills, applies discounts and GST, and stores stock and billing records in plain-text files.

## Project Information

- **Project:** Project 4 – Grocery Billing and Stock Manager
- **Group:** Group 4
- **Members:** Parth Gupta, Piyush Kumar, Mohd. Arshad Ali, Manikanta Narukulla
- **Core Concepts:** Recursion, File Handling, Exception Handling, Conditional Statements (`if`/`elif`/`else`)

## Project Files

| File | Description |
|---|---|
| `grocery_billing_manager.py` | Main Python program containing the menu, stock management, recursive billing, calculations, and file-handling logic. |
| `README.md` | Project documentation. |
| `stock.txt` | Stock data file created/updated by the application when stock is saved. |
| `bills.txt` | Append-only file containing saved bills. |

`stock.txt` and `bills.txt` are runtime data files. If `stock.txt` does not exist or is empty, the program starts with its built-in default stock.

## Requirements

- Python 3
- No third-party packages are required. The program uses Python built-in functionality only.

## Run the Application

From the project directory, run:

```bash
python grocery_billing_manager.py

## Main Menu
============================================
     GROCERY BILLING AND STOCK MANAGER      
============================================
  [1] View stock by category
  [2] Create a customer bill
  [3] Add a new item
  [4] Restock an existing item
  [5] Low stock report
  [6] View saved bills
  [7] Save stock now
  [8] Save & Exit
--------------------------------------------
## FEATURS
================================STOCK MANAGEMENT====================================================

🏁 Displays stock grouped into the categories beverages, dairy, grains, snacks, and vegetables.
  
🏁 Adds new items with a category, price, unit, and starting quantity.

🏁Restocks existing items by adding to their current quantity.

🏁Warns when an item's remaining quantity is at or below the low-stock limit.

🏁Displays a separate low-stock report.

🏁Automatically saves stock updates after adding new items, restocking, creating a bill, or exiting.

### BILLING ####
🟢Creates a bill recursively by entering item names and quantities.
🟢Checks available stock before accepting a quantity.
🟢Reduces stock as items are added to a bill.
🟢Supports these commands while creating a bill:
🟢done — finish entering items and generate the bill.
🟢remove — remove the last added item and return its quantity to stock.
🟢cancel — cancel the bill and return all quantities entered for that bill to stock.
🟢Displays a formatted bill with item, quantity, rate, amount, subtotal, discount, GST, and grand total.
🟢Displays the top three billed items by line amount.

### Billing Rule ###

🧾 Billing Rules & Tax Calculation

| 🏷️ Rule / Parameter | ⚙️ Constant | 📊 Configured Value | 📝 Condition |
| :--- | :---: | :---: | :--- |
| **Discount Threshold** | `DISCOUNT_LIMIT` | **₹1,000.00** | Minimum subtotal required to unlock discount |
| **Bulk Discount** | `DISCOUNT` | **10%** | Deducted from subtotal when `Subtotal >= ₹1,000` |
| **Goods & Services Tax** | `GST` | **5%** | Applied on the discounted taxable amount |
| **Low-Stock Alert** | `LOW` | **≤ 5 units** | Triggers restock warning in stock list & billing |

### 🧮 Step-by-Step Billing Formula
┌──────────────────────────────────────────────────────────────────┐
│  1. Subtotal       =  Σ (Item Quantity × Unit Rate)              │
│  2. Discount       =  10% of Subtotal   (if Subtotal >= ₹1,000)  │
│                       ₹0.00             (if Subtotal <  ₹1,000)  │
│  3. Taxable Amount =  Subtotal − Discount                        │
│  4. GST (5%)       =  5% of Taxable Amount                       │
│  ──────────────────────────────────────────────────────────────  │
│  💰 GRAND TOTAL    =  Taxable Amount + GST                       │
└──────────────────────────────────────────────────────────────────┘

## Default Stock

## Default Stock
--When no usable `stock.txt` file is available, the program loads this built-in starting stock:
| Item | Category | Price | Unit | Quantity |
|---|---|---:|---|---:|
| Rice | Grains | Rs 60 | kg | 50 |
| Wheat flour | Grains | Rs 45 | kg | 40 |
| Milk | Dairy | Rs 28 | packet | 30 |
| Butter | Dairy | Rs 55 | piece | 4 |
| Biscuits | Snacks | Rs 10 | packet | 60 |
| Chips | Snacks | Rs 20 | packet | 25 |
| Tea | Beverages | Rs 120 | packet | 15 |
| Potato | Vegetables | Rs 30 | kg | 35 |

## Data Storage

The application stores data in the current working directory:

- **`stock.txt`** — one stock record per line, sorted alphabetically by item name, with fields separated by `|`:

  ```text
  item_name|category|price|unit|quantity

## TESTING ###

The source file's module docstring mentions running doctests with:

```bash
python -m doctest -v grocery_billing_manager.py
```

That command assumes the source file has been renamed to `grocery_billing_manager.py`. The supplied source currently contains no doctest examples, so this command may complete without running any tests.

## Notes ##
-Prices and bill totals are displayed in rupees (Rs).
-Item names and categories are normalized to lowercase with extra spaces removed for lookup.
-Viewing saved bills (past_bills) displays the last 20 lines of bills.txt.
-The program is terminal/command-line based; it does not include a graphical interface or database.
-Stock and bills are plain-text files, not a database.
