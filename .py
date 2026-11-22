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


# ---------- FILE HANDLING + EXCEPTION HANDLING ----------
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
