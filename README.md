Grocery Billing and Stock Manager
A menu-driven Python application for managing a small grocery shop. It maintains item stock, creates customer bills, applies discounts and GST, and stores stock and billing records in plain-text files.
Project Files
File	Description
.py	Main Python program containing the menu, stock management, billing, calculations, and file-handling logic.
README.md	Project documentation.
stock.txt	Stock data file created/updated by the application when stock is saved.
bills.txt	Append-only file containing saved bills.


stock.txt and bills.txt are runtime data files. If stock.txt does not exist or is empty, the program starts with its built-in default stock.
Requirements
- Python 3
- No third-party packages are required. The program uses Python built-in functionality only.
Run the Application
The Python source file in the supplied project archive is named .py. From the project directory, run:
python .py
Alternatively, rename .py to grocery_billing_manager.py and run:
python grocery_billing_manager.py
The application starts by loading stock and displaying the main menu.
Main Menu
Option	Function
1	View stock, grouped by category
2	Create a bill
3	Add a new item
4	Restock an existing item
5	Display the low-stock report
6	View saved bills
7	Save stock immediately
8	Save stock and exit


Features
Stock Management
- Displays stock grouped into the categories grains, dairy, snacks, beverages, and vegetables.
- Adds new items with a category, price, unit, and starting quantity.
- Restocks existing items.
- Warns when an item's remaining quantity is at or below the low-stock limit.
- Displays a separate low-stock report.
Billing
- Creates a bill by entering item names and quantities.
- Checks available stock before accepting a quantity.
- Reduces stock as items are added to a bill.
- Supports these commands while creating a bill:
  - done — finish entering items.
  - remove — remove the last added item and return its quantity to stock.
  - cancel — cancel the bill and return all quantities entered for that bill to stock.
- Displays a formatted bill with item, quantity, rate, amount, subtotal, discount, GST, and grand total.
- Displays the top three billed items by line amount.
Billing Rules
The values below are defined in the program's constants:
Rule	Value
GST	5%
Discount threshold	Subtotal of Rs 1,000 or more
Discount	10% of subtotal when the threshold is reached
Low-stock threshold	Quantity of 5 or fewer


The discount is deducted from the subtotal first. GST is then calculated on the discounted taxable amount.

Calculation:
Discount = 10% of subtotal, if subtotal >= Rs 1,000; otherwise Rs 0
Taxable amount = Subtotal - Discount
GST = 5% of taxable amount
Grand total = Taxable amount + GST
Default Stock
When no usable stock file is available, the program loads this built-in starting stock:
Item	Category	Price	Unit	Quantity
Rice	Grains	Rs 60	kg	50
Wheat flour	Grains	Rs 45	kg	40
Milk	Dairy	Rs 28	packet	30
Butter	Dairy	Rs 55	piece	4
Biscuits	Snacks	Rs 10	packet	60
Chips	Snacks	Rs 20	packet	25
Tea	Beverages	Rs 120	packet	15
Potato	Vegetables	Rs 30	kg	35


Data Storage
The application stores data in the current working directory:
- stock.txt — one stock record per line, with fields separated by |:
  item_name|category|price|unit|quantity
- bills.txt — saved bills in readable, formatted text. New bills are appended to this file.
The application handles missing or unreadable stock files by falling back to the default stock. It also skips malformed stock-file lines and reports them.
Testing
The source file's module docstring mentions running doctests with:
python -m doctest -v grocery_billing_manager.py
That command assumes the source file has been renamed to grocery_billing_manager.py. The supplied source currently contains no doctest examples, so this command may complete without running any tests.
Notes
- Prices and bill totals are displayed in rupees (Rs).
- Item names and categories are normalized to lowercase for lookup.
- The program is terminal/command-line based; it does not include a graphical interface or database.
- Stock and bills are plain-text files, not a database.