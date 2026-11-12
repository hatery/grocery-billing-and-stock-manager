"""
Project 4: Grocery Billing and Stock Manager  (Group 4)

A menu-driven program for a small grocery shop.
No modules are imported; only built-in functions are used.
Data is saved in plain .txt files (stock.txt and bills.txt).

Run the doctests with:  python -m doctest -v grocery_billing_manager.py
"""

# ---------------------------------------------------------------- constants
STOCK_FILE = "stock.txt"
BILL_FILE = "bills.txt"
GST_PERCENT = 5            # GST added on every bill
DISCOUNT_LIMIT = 1000.0    # discount applies when subtotal reaches this
DISCOUNT_PERCENT = 10      # discount percentage
LOW_STOCK_LIMIT = 5        # warn when quantity is at or below this

# A set of item categories (unique, quick-lookup data)
CATEGORIES = {"grains", "dairy", "snacks", "beverages", "vegetables"}


DEFAULT_STOCK = {
    "rice": {"price_unit": (60.0, "kg"), "qty": 50, "category": "grains"},
    "wheat flour": {"price_unit": (45.0, "kg"), "qty": 40, "category": "grains"},
    "milk": {"price_unit": (28.0, "packet"), "qty": 30, "category": "dairy"},
    "butter": {"price_unit": (55.0, "piece"), "qty": 4, "category": "dairy"},
    "biscuits": {"price_unit": (10.0, "packet"), "qty": 60, "category": "snacks"},
    "chips": {"price_unit": (20.0, "packet"), "qty": 25, "category": "snacks"},
    "tea": {"price_unit": (120.0, "packet"), "qty": 15, "category": "beverages"},
    "potato": {"price_unit": (30.0, "kg"), "qty": 35, "category": "vegetables"},
}


# ---------------------------------------------------------- input helpers
def clean_text(text):
    """Strip extra spaces and make the text lower case.

    >>> clean_text("   Wheat   FLOUR ")
    'wheat   flour'
    >>> clean_text("")
    ''
    """
    return text.strip().lower()


def normalise_name(text):
    """Clean an item name and squeeze repeated inner spaces using split/join.

    >>> normalise_name("  Wheat    FLOUR ")
    'wheat flour'
    """
    return " ".join(clean_text(text).split())


def read_positive_int(prompt):
    """Ask until the user types a whole number greater than zero."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("  Invalid input. Please enter a whole number above 0.")


def read_positive_float(prompt):
    """Ask until the user types a number greater than zero (e.g. 12.50)."""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
            if value > 0:
                return value
            print("  The value must be greater than 0.")
        except ValueError:
            print("  Invalid input. Please enter a number such as 25 or 12.5.")


def read_nonempty(prompt):
    """Ask until the user types something that is not empty; return it cleaned."""
    while True:
        text = normalise_name(input(prompt))
        if text != "":
            return text
        print("  Input cannot be empty. Try again.")


#  calculations
def total_amounts(amounts):

    if len(amounts) == 0:         
        return 0
    return amounts[0] + total_amounts(amounts[1:])


def calculate_charges(subtotal):
    """Return (discount, gst, grand_total) for a bill subtotal.

    A discount is given only when the subtotal reaches DISCOUNT_LIMIT.
    GST is charged on the amount after discount.

    >>> calculate_charges(500.0)
    (0.0, 25.0, 525.0)
    >>> calculate_charges(2000.0)
    (200.0, 90.0, 1890.0)
    """
    if subtotal >= DISCOUNT_LIMIT:
        discount = subtotal * DISCOUNT_PERCENT / 100
    else:
        discount = 0.0
    taxable = subtotal - discount
    gst = taxable * GST_PERCENT / 100
    return discount, gst, taxable + gst


def is_low_stock(quantity):
    """Return True when the quantity is at or below the low-stock limit.

    >>> is_low_stock(3)
    True
    >>> is_low_stock(50)
    False
    """
    return quantity <= LOW_STOCK_LIMIT


#  file handling
def next_bill_number(filename):
    """Return the next bill number by counting the bills already saved.

    The first bill is 1001. A missing or unreadable file also gives 1001.
    """
    try:
        with open(filename, "r") as file:
            saved_bills = file.read().count("GROCERY BILL")
    except OSError:
        saved_bills = 0
    return 1001 + saved_bills


def load_stock(filename):
    """Load stock from a text file (name|category|price|unit|qty per line).

    If the file is missing, the default stock is returned instead.
    Bad lines are skipped with a message; the program never crashes.
    """
    stock = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                try:
                    name, category, price, unit, qty = line.split("|")
                    if category not in CATEGORIES:
                        raise ValueError("unknown category")
                    stock[name] = {
                        "price_unit": (float(price), unit),
                        "qty": int(qty),
                        "category": category,
                    }
                except ValueError:
                    print("  Skipped a damaged line in", filename + ":", line)
    except FileNotFoundError:
        print("  No stock file found. Starting with default stock.")
        return dict(DEFAULT_STOCK)
    except OSError:
        print("  Could not read the stock file. Using default stock.")
        return dict(DEFAULT_STOCK)
    if len(stock) == 0:
        print("  Stock file was empty. Using default stock.")
        return dict(DEFAULT_STOCK)
    return stock


def save_stock(stock, filename):
    """Write the whole stock dictionary to a text file. Return True if saved."""
    try:
        with open(filename, "w") as file:
            for name in sorted(stock):
                record = stock[name]
                price, unit = record["price_unit"]
                line = "|".join([name, record["category"], str(price), unit,
                                 str(record["qty"])])
                file.write(line + "\n")
        return True
    except OSError:
        print("  Error: could not save the stock file.")
        return False


def save_bill(lines, filename):
    """Append the bill text (a list of strings) to the bills file."""
    try:
        with open(filename, "a") as file:
            for line in lines:
                file.write(line + "\n")
            file.write("\n")
        return True
    except OSError:
        print("  Error: could not save the bill file.")
        return False


# formatting
def format_cell(value, width):
    """Format one table cell: numbers right-aligned, text left-aligned.

    >>> format_cell("rice", 8)
    'rice    '
    >>> format_cell(12.5, 8)
    '   12.50'
    """
    if isinstance(value, float):
        return f"{value:.2f}".rjust(width)
    if isinstance(value, int):
        return str(value).rjust(width)
    return str(value).ljust(width)


def build_bill_lines(bill_no, records, subtotal, discount, gst, grand_total):
    """Build the bill as a list of text lines (used for screen and file).

    The table is printed with nested loops: one loop over records and an
    inner loop over the fields of each record.
    """
    widths = [18, 6, 10, 12]
    headings = ["Item", "Qty", "Rate", "Amount"]
    line = "-" * 46
    lines = ["=" * 46, f"GROCERY BILL  No. {bill_no}".center(46), "=" * 46]

    header = ""
    for index in range(len(headings)):
        header += headings[index].ljust(widths[index])
    lines.extend([header, line])

    for record in records:                       # outer loop: each item
        row = ""
        for index in range(len(record)):         # inner loop: each field
            row += format_cell(record[index], widths[index])
        lines.append(row)

    lines.append(line)
    lines.append("Subtotal".ljust(34) + f"{subtotal:>12.2f}")
    lines.append(f"Discount ({DISCOUNT_PERCENT}%)".ljust(34) + f"{-discount:>12.2f}")
    lines.append(f"GST ({GST_PERCENT}%)".ljust(34) + f"{gst:>12.2f}")
    lines.append("=" * 46)
    lines.append("GRAND TOTAL".ljust(34) + f"{grand_total:>12.2f}")
    lines.append("=" * 46)
    return lines



def show_stock(stock):
    """Print stock grouped by category using nested loops."""
    print("\n" + "STOCK BY CATEGORY".center(54))
    for category in sorted(CATEGORIES):              # outer loop: categories
        print("\n[" + category.title() + "]")
        found = False
        for name in sorted(stock):                   # inner loop: items
            record = stock[name]
            if record["category"] == category:
                price, unit = record["price_unit"]
                note = "  <-- LOW STOCK" if is_low_stock(record["qty"]) else ""
                print(f"  {name.title():<16} Rs {price:>7.2f}/{unit:<7}"
                      f" Qty: {record['qty']:>4}{note}")
                found = True
        if not found:
            print("  (no items)")


def add_new_item(stock):
    """Add a brand new item to the stock dictionary."""
    name = read_nonempty("Item name: ")
    if name in stock:
        print("  That item already exists. Use 'Restock' instead.")
        return
    category = read_nonempty("Category (" + ", ".join(sorted(CATEGORIES)) + "): ")
    if category not in CATEGORIES:
        print("  Unknown category. Item not added.")
        return
    price = read_positive_float("Price per unit (Rs): ")
    unit = read_nonempty("Unit (kg / packet / piece / litre): ")
    qty = read_positive_int("Quantity in stock: ")
    stock[name] = {"price_unit": (price, unit), "qty": qty, "category": category}
    print("  Added", name.title() + ".")


def restock_item(stock):
    """Increase the quantity of an existing item."""
    name = read_nonempty("Item to restock: ")
    if name not in stock:
        print("  Item not found.")
        return
    amount = read_positive_int("Quantity to add: ")
    stock[name]["qty"] += amount
    print(f"  {name.title()} now has {stock[name]['qty']} in stock.")


# ---------------------------------------------------------------- billing
def put_back(stock, record):
    """Return the quantity of a removed bill record to the stock."""
    stock[record[0].lower()]["qty"] += record[1]


def create_bill(stock):
    """Create a bill for several items; update stock and save the files."""
    records = []        # list of records: [name, qty, rate, amount]
    print("\nType item names to add to the bill.")
    print("Commands: 'done' = finish, 'remove' = remove last item, "
          "'cancel' = cancel bill")

    while True:
        command = normalise_name(input("\nItem name / command: "))
        if command == "":
            print("  Input cannot be empty. Try again.")
        elif command == "done":
            break
        elif command == "cancel":
            for record in records:
                put_back(stock, record)
            print("  Bill cancelled.")
            return
        elif command == "remove":
            if len(records) == 0:
                print("  Nothing to remove.")
            else:
                removed = records[-1]
                records.remove(removed)
                put_back(stock, removed)
                print("  Removed", removed[0] + ".")
        elif command not in stock:
            print("  Item not found. Check the stock list (option 1).")
        else:
            available = stock[command]["qty"]
            if available == 0:
                print("  Out of stock.")
                continue
            qty = read_positive_int(f"Quantity ({available} available): ")
            if qty > available:
                print("  Not enough stock. Only", available, "left.")
                continue
            rate = stock[command]["price_unit"][0]
            records.append([command.title(), qty, rate, qty * rate])
            stock[command]["qty"] -= qty
            if is_low_stock(stock[command]["qty"]):
                print(f"  WARNING: only {stock[command]['qty']} "
                      f"{command.title()} left. Please restock!")

    if len(records) == 0:
        print("  Empty bill. Nothing saved.")
        return

    # Recursive total of all amounts, then discount and GST
    subtotal = total_amounts([record[3] for record in records])
    discount, gst, grand_total = calculate_charges(subtotal)
    bill_no = next_bill_number(BILL_FILE)

    lines = build_bill_lines(bill_no, records, subtotal, discount, gst, grand_total)
    print()
    for line in lines:
        print(line)

    # Slicing + sort: show the three biggest items of this bill
    ranked = sorted(records, key=lambda rec: rec[3], reverse=True)
    top_names = [rec[0] for rec in ranked[:3]]
    print("Top items by amount:", ", ".join(top_names))
    if discount > 0:
        print(f"You saved Rs {discount:.2f} with the discount!")

    if save_bill(lines, BILL_FILE) and save_stock(stock, STOCK_FILE):
        print("Bill saved to", BILL_FILE, "and stock updated in", STOCK_FILE)


def show_low_stock(stock):
    """Print every item whose stock is low."""
    low_items = [name for name in sorted(stock) if is_low_stock(stock[name]["qty"])]
    if len(low_items) == 0:
        print("\n  All items are well stocked.")
        return
    print("\nLOW STOCK ITEMS")
    for name in low_items:
        print(f"  {name.title():<16} only {stock[name]['qty']} left")


def show_past_bills():
    """Show the last part of the bills file (last 20 lines by slicing)."""
    try:
        with open(BILL_FILE, "r") as file:
            all_lines = file.read().split("\n")
    except FileNotFoundError:
        print("  No bills have been saved yet.")
        return
    except OSError:
        print("  Could not read the bills file.")
        return
    print()
    for line in all_lines[-20:]:
        print(line)


# ------------------------------------------------------------------- main
def show_menu():
    """Print the main menu."""
    print("\n" + "=" * 40)
    print("  GROCERY BILLING AND STOCK MANAGER")
    print("=" * 40)
    print(" 1. View stock")
    print(" 2. Create a bill")
    print(" 3. Add a new item")
    print(" 4. Restock an item")
    print(" 5. Low stock report")
    print(" 6. View saved bills")
    print(" 7. Save stock now")
    print(" 8. Exit")


def main():
    """Run the main menu loop until the user chooses Exit."""
    stock = load_stock(STOCK_FILE)
    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()
        if not choice.isdigit():
            print("  Please type a number from 1 to 8.")
        elif choice == "1":
            show_stock(stock)
        elif choice == "2":
            create_bill(stock)
        elif choice == "3":
            add_new_item(stock)
            save_stock(stock, STOCK_FILE)
        elif choice == "4":
            restock_item(stock)
            save_stock(stock, STOCK_FILE)
        elif choice == "5":
            show_low_stock(stock)
        elif choice == "6":
            show_past_bills()
        elif choice == "7":
            if save_stock(stock, STOCK_FILE):
                print("  Stock saved.")
        elif choice == "8":
            save_stock(stock, STOCK_FILE)
            print("Stock saved. Goodbye!")
            break
        else:
            print("  Invalid choice. Please pick a number from 1 to 8.")


if __name__ == "__main__":
    main()