"""
Project 4: Grocery Billing and Stock Manager  (Group 4)
Group Members-
        Parth Gupta
        Piyush Kumar
        Mohd. Arshad Ali
        Manikanta Chaudhary
A menu-driven program for a small grocery shop.
No modules are imported; only built-in functions are used.
Data is saved in plain .txt files (stock.txt and bills.txt).
Run the doctests with:  python -m doctest -v grocery_billing_manager.py
"""


# ---------------------------------------------------------------------------
STOCK_FILE = "stock.txt"
BILL_FILE = "bills.txt"
GST_PERCENT = 5            
DISCOUNT_LIMIT = 1000.0   
DISCOUNT_PERCENT = 10     
LOW_STOCK_LIMIT = 5        
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


def get_default_stock():
    return {name: dict(details) for name, details in DEFAULT_STOCK.items()}
def clean_text(text):
    return text.strip().lower()
def normalise_name(text):
    return " ".join(clean_text(text).split())
def read_positive_int(prompt):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("  Invalid input. Please enter a whole number above 0.")
def read_positive_float(prompt):
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
            if value > 0:
                return value
            print("  The value must be greater than 0.")
        except ValueError:
            print(" Invalid input. Please enter a number such as 25 or 12.5.")

def read_nonempty(prompt):
    while True:
        text = normalise_name(input(prompt))
        if text != "":
            return text
        print("Input cannot be empty. Try again.")

def calculate_charges(subtotal):
    if subtotal >= DISCOUNT_LIMIT:
        discount = subtotal * DISCOUNT_PERCENT / 100
    else:
        discount = 0.0
    taxable = subtotal - discount
    gst = taxable * GST_PERCENT / 100
    return discount, gst, taxable + gst

def is_low_stock(quantity):
    return quantity <= LOW_STOCK_LIMIT

def next_bill_number(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            saved_bills = file.read().count("GROCERY BILL")
    except OSError:
        saved_bills = 0
    return 1001 + saved_bills

def load_stock(filename):
    stock = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
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
        return get_default_stock()
    except OSError:
        print("  Could not read the stock file. Using default stock.")
        return get_default_stock()
    if len(stock) == 0:
        print("  Stock file was empty. Using default stock.")
        return get_default_stock()
    return stock

def save_stock(stock,filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for name in sorted(stock):
                record = stock[name]
                price, unit = record["price_unit"]
                line = "|".join([
                    name,
                    record["category"],
                    str(price),
                    unit,
                    str(record["qty"]),
                ])
                file.write(line + "\n")
        return True
    except OSError:
        print("Error: could not save the stock file.")
        return False

def save_bill(lines, filename):
    try:
        with open(filename,"a", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")
            file.write("\n")
        return True
    except OSError:
        print("Error: could not save the bill file.")
        return False

def format_cell(value, width):
    if isinstance(value, float):
        return f"{value:.2f}".rjust(width)
    if isinstance(value, int):
        return str(value).rjust(width)
    return str(value).ljust(width)

def build_bill_lines(bill_no, records, subtotal, discount, gst, grand_total):
    widths = [18, 6, 10, 12]
    headings = ["Item", "Qty", "Rate", "Amount"]
    line = "-" * 46
    lines = ["=" * 46, f"Grocery Bill  No. {bill_no}".center(46), "=" * 46]

    header = ""
    for index in range(len(headings)):
        header += headings[index].ljust(widths[index])
    lines.extend([header, line])

    for record in records:
        row = ""
        for index in range(len(record)):
            row += format_cell(record[index], widths[index])
        lines.append(row)

    lines.append(line)
    lines.append("Subtotal".ljust(34) + f"{subtotal:>12.2f}")
    lines.append(f"Discount ({DISCOUNT_PERCENT}%)".ljust(34) + f"{-discount:>12.2f}")
    lines.append(f"GST ({GST_PERCENT}%)".ljust(34) + f"{gst:>12.2f}")
    lines.append("=" * 46)
    lines.append("Grand Total: ".ljust(34) + f"{grand_total:>12.2f}")
    lines.append("=" * 46)
    return lines


def show_stock(stock):
    print("\n" + "STOCK BY CATEGORY".center(54))
    for category in sorted(CATEGORIES):
        print("\n["+ category.title()+"]")
        found = False
        for name in sorted(stock):
            record = stock[name]
            if record["category"] == category:
                price, unit = record["price_unit"]
                note = "  <-- LOW STOCK" if is_low_stock(record["qty"]) else ""
                print(
                    f" {name.title():<16} Rs {price:>7.2f}/{unit:<7}"
                    f" Qty: {record['qty']:>4}{note}"
                )
                found = True
        if not found:
            print(" (no items)")


def add_new_item(stock):
    name = read_nonempty("Item name: ")
    if name in stock:
        print("  That item already exists. Use 'Restock' instead.")
        return
    category = read_nonempty("Category (" + ", ".join(sorted(CATEGORIES)) + "): ")
    if category not in CATEGORIES:
        print(" Unknown category. Item not added.")
        return
    price = read_positive_float("Price per unit (Rs): ")
    unit = read_nonempty("Unit (kg / packet / piece / litre): ")
    qty = read_positive_int("Quantity in stock: ")
    stock[name] = {"price_unit": (price, unit), "qty": qty, "category": category}
    print(" Added", name.title() + ".")


def restock_item(stock):
    name = read_nonempty("Item to restock: ")
    if name not in stock:
        print(" Item not found.")
        return
    amount = read_positive_int("Quantity to add: ")
    stock[name]["qty"] += amount
    print(f" {name.title()} now has {stock[name]['qty']} is there in stock.")


def put_back(stock, record):
    stock[record[0].lower()]["qty"] += record[1]


def create_bill(stock):
    records = []
    print("\nType item names to add to the bill.")
    print("Commands: 'done' = finish, 'remove' = remove last item, "
        "'cancel' = cancel bill")

    while True:
        command = normalise_name(input("\nItem name / command: "))
        if command == "":
            print("Input can't be empty. Enter again.")
        elif command == "done":
            break
        elif command == "cancel":
            for record in records:
                put_back(stock, record)
            print(" Bill cancelled.")
            return
        elif command == "remove":
            if len(records) == 0:
                print("Nothing to Remove.")
            else:
                removed = records.pop()
                put_back(stock, removed)
                print("  Removed", removed[0] + ".")
        elif command not in stock:
            print(" Item not found. Check the stock list (option 1).")
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
                print(
                    f" WARNING: only {stock[command]['qty']} "
                    f"{command.title()} left. Please restock!"
                )

    if len(records) == 0:
        print(" Empty bill. Nothing saved.")
        return

    subtotal = sum(record[3] for record in records)
    discount, gst, grand_total = calculate_charges(subtotal)
    bill_no = next_bill_number(BILL_FILE)

    lines = build_bill_lines(bill_no, records, subtotal, discount, gst, grand_total)
    print()
    for line in lines:
        print(line)

    ranked = sorted(records, key=lambda rec: rec[3], reverse=True)
    top_names = [rec[0] for rec in ranked[:3]]
    print("Top items by amount:", ", ".join(top_names))
    if discount > 0:
        print(f"You saved Rs {discount:.2f} with the discount!")

    if save_bill(lines, BILL_FILE) and save_stock(stock, STOCK_FILE):
        print("Bill saved to", BILL_FILE, "and stock updated in", STOCK_FILE)


def show_low_stock(stock):
    low_items = [name for name in sorted(stock) if is_low_stock(stock[name]["qty"])]
    if len(low_items) == 0:
        print("\n  All items are well stocked.")
        return
    print("\nLOW STOCK ITEMS")
    for name in low_items:
        print(f" {name.title():<16} only {stock[name]['qty']} left")


def show_past_bills():
    try:
        with open(BILL_FILE, "r", encoding="utf-8") as file:
            all_lines = file.read().split("\n")
    except FileNotFoundError:
        print("  No bills have been saved yet.")
        return
    except OSError:
        print(" Could not read the bills file.")
        return
    print()
    for line in all_lines[-20:]:
        print(line)


def show_menu():
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
            print(" Invalid choice. Please pick a number from 1 to 8.")


if __name__ == "__main__":
    main()


