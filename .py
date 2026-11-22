"""Project 4: Grocery Billing and Stock Manager (Group 4)
-------Members-----------:
    Parth Gupta
    Piyush Kumar
    Mohd. Arshad Ali
    Manikanta Narukulla
------------------------------
"""
STOCK_FILE, BILL_FILE = "stock.txt", "bills.txt"
GST, DISCOUNT, DISCOUNT_LIMIT, LOW = 5, 10, 1000, 5
CATEGORIES = ["beverages", "dairy", "grains", "snacks", "vegetables"]
DEFAULT = {  # name: [price, unit, qty, category]
    "rice": [60.0, "kg", 50, "grains"], "wheat flour": [45.0, "kg", 40, "grains"],
    "milk": [28.0, "packet", 30, "dairy"], "butter": [55.0, "piece", 4, "dairy"],
    "biscuits": [10.0, "packet", 60, "snacks"], "chips": [20.0, "packet", 25, "snacks"],
    "tea": [120.0, "packet", 15, "beverages"], "potato": [30.0, "kg", 35, "vegetables"]}
def load_stock():
    stock = {}
    try:
        with open(STOCK_FILE) as f:
            for line in f:                      
                try:
                    n,c,p,u,q = line.strip().split("|")
                    stock[n] = [float(p),u,int(q),c]
                except ValueError:
                    print("Skipped the faulty line:", line.strip())
    except FileNotFoundError:
        print("  Stock file not found. Default stock is being used.")
    return stock or {n: d[:] for n, d in DEFAULT.items()}
def save_stock(stock):
    try:
        with open(STOCK_FILE, "w") as f:
            for n in sorted(stock):
                p, u, q, c = stock[n]
                f.write(f"{n}|{c}|{p}|{u}|{q}\n")
        return True
    except OSError:
        print("  Error: stock not saved.")

def read_file(name):
    try:
        with open(name) as f:
            return f.read()
    except OSError:
        return ""
# ---------- RECURSION ----------
def read_number(prompt, kind):
    """Sahi number milne tak khud ko dobara call karta hai."""
    try:
        value = kind(input(prompt))
        if value > 0:
            return value
        print("  Number should be greater than 0.")
    except ValueError:
        print("  Wrong input. Write correct number.")
    return read_number(prompt, kind)

def total_amount(records):
    return 0 if not records else records[0][3] + total_amount(records[1:])
    
def put_back(stock, records):
    if records:
        stock[records[0][0].lower()][2] += records[0][1]
        put_back(stock, records[1:])
def add_items(stock, records):
    cmd = " ".join(input("\nItem name / command: ").lower().split())
    if cmd == "done":                           
        return records
    elif cmd == "cancel":
        put_back(stock, records)
        print("  Bill cancelled.")
        return None
    elif cmd == "remove":
        if records:
            put_back(stock, [records.pop()])
            print("Last item removed")
        else:
            print(" Nothing is there to remove .")
    elif cmd not in stock:
        print(" Item not found See Stock list (option 1)")
    elif stock[cmd][2] == 0:
        print("Out of stock")
    else:
        item = stock[cmd]
        qty = read_number(f"Quantity ({item[2]} available): ", int)
        if qty > item[2]:
            print(" Not enough stock. Only", item[2], "is left")
        else:
            item[2] -= qty
            records.append([cmd.title(), qty, item[0], qty * item[0]])
            if item[2] <= LOW:
                print(f"  WARNING: only {item[2]} {cmd.title()} is left. Do Restock !")
    return add_items(stock, records)


# ---------- BILL ----------
def create_bill(stock):
    print("\nWrite item name to add in bill.")
    print("Commands: 'done' = finish, 'remove' = remove last item , 'cancel' = bill cancel")
    records = add_items(stock, [])
    if records is None:
        return
    if not records:
        print("  Bill is empty. Nothing is saved.")
        return

    subtotal = total_amount(records)
    discount = subtotal * DISCOUNT / 100 if subtotal >= DISCOUNT_LIMIT else 0.0
    gst = (subtotal - discount) * GST / 100
    bill_no = 1001 + read_file(BILL_FILE).count("GROCERY BILL")

    line, bar = "-" * 46, "=" * 46
    lines = [bar, f"GROCERY BILL  No. {bill_no}".center(46), bar,
             f"{'Item':<18}{'Qty':>6}{'Rate':>10}{'Amount':>12}", line]
    lines += [f"{n:<18}{q:>6}{r:>10.2f}{a:>12.2f}" for n, q, r, a in records]
    lines += [line, f"{'Subtotal':<34}{subtotal:>12.2f}",
              f"{f'Discount ({DISCOUNT}%)':<34}{-discount:>12.2f}",
              f"{f'GST ({GST}%)':<34}{gst:>12.2f}", bar,
              f"{'GRAND TOTAL':<34}{subtotal - discount + gst:>12.2f}", bar]
    print("\n" + "\n".join(lines))

    top = sorted(records, key=lambda r: r[3], reverse=True)[:3]
    print("Top items by amount:", ", ".join(r[0] for r in top))
    if discount > 0:
        print(f"You saved Rs {discount:.2f} with the discount!")
    try:
        with open(BILL_FILE, "a") as f:
            f.write("\n".join(lines) + "\n\n")
        if save_stock(stock):
            print("Bill saved to", BILL_FILE, "and stock updated in", STOCK_FILE)
    except OSError:
        print("Error: bill save nahi hua")


