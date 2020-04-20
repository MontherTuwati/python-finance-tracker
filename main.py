import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import init_db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime

init_db()

# Database
def insert_transaction(date, category, amount, notes, upcoming, payment_type):
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (date, category, amount, notes, upcoming, payment_type)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (date, category, amount, notes, upcoming, payment_type)
    )
    conn.commit()
    conn.close()
    refresh_table()


def fetch_transactions():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_category_total(cat):
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE category=?", (cat,))
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0.0

def generate_chart():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, SUM(amount) FROM transactions GROUP BY date ORDER BY date")
    data = cursor.fetchall()
    conn.close()

    if not data:
        return None

    dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d").date() for row in data]
    totals = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(4.5, 2.5))
    ax.plot(dates, totals, marker='o', linestyle='-', color="#4CAF50")
    ax.set_title("Expenses Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Spent")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

    return fig

# Category data
category_data = {
    "Food": {"emoji": "🍔", "color": "#ffe4b3"},
    "Rent": {"emoji": "🏠", "color": "#e6e6fa"},
    "Transport": {"emoji": "🚗", "color": "#d0f0c0"},
    "Bills": {"emoji": "💡", "color": "#ffd6cc"},
    "Healthcare": {"emoji": "💊", "color": "#ffe6e6"},
    "Education": {"emoji": "📚", "color": "#e0f7ff"},
    "Investment": {"emoji": "💰", "color": "#fff7cc"},
    "Other": {"emoji": "🧾", "color": "#f0e6ff"}
}

# Add transaction form
def open_add_transaction():
    def submit():
        date = date_entry.get()
        category = category_var.get()
        amount_raw = amount_entry.get().strip()
        notes = notes_entry.get()
        upcoming = 1 if upcoming_var.get() else 0
        payment_type = payment_type_var.get()

        try:
            amount = float(amount_raw)
            insert_transaction(date, category, amount, notes, upcoming, payment_type)
            form.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", f"Amount must be a number. You entered: '{amount_raw}'")

    form = tk.Toplevel(root)
    form.title("Add Transaction")
    form.geometry("350x350")
    form.config(bg="white")

    tk.Label(form, text="Date (YYYY-MM-DD):", bg="white").pack(pady=(10, 0))
    date_entry = tk.Entry(form, width=30)
    date_entry.pack()

    tk.Label(form, text="Category:", bg="white").pack(pady=(10, 0))
    category_var = tk.StringVar()
    category_menu = ttk.Combobox(form, textvariable=category_var, values=list(category_data.keys()), state="readonly")
    category_menu.pack()

    tk.Label(form, text="Amount:", bg="white").pack(pady=(10, 0))
    amount_entry = tk.Entry(form, width=30)
    amount_entry.pack()

    tk.Label(form, text="Notes:", bg="white").pack(pady=(10, 0))
    notes_entry = tk.Entry(form, width=30)
    notes_entry.pack()

    tk.Label(form, text="Payment Type:", bg="white").pack(pady=(10, 0))
    payment_type_var = tk.StringVar(value="Cash")
    payment_menu = ttk.Combobox(form, textvariable=payment_type_var, values=["Cash", "Card"], state="readonly")
    payment_menu.pack()

    upcoming_var = tk.IntVar()
    tk.Checkbutton(form, text="Mark as Upcoming Transaction", variable=upcoming_var, bg="white").pack(pady=(10, 0))

    tk.Button(form, text="Submit", command=submit, bg="#4CAF50", fg="white").pack(pady=15)

# Main window
root = tk.Tk()
root.title("Finance Tracker Dashboard")
root.geometry("1000x750")
root.configure(bg="#f5f7fa")

# ────────────────────────
# 🔼 Top Section Updated
# ────────────────────────
top_frame = tk.Frame(root, bg="#d9f2e6", height=280)
top_frame.pack(fill="x")

# Profile-style card (left)
profile_frame = tk.Frame(top_frame, bg="white", width=300, height=220, bd=1, relief="ridge")
profile_frame.place(x=30, y=30)
profile_frame.grid_propagate(False)

avatar_canvas = tk.Canvas(profile_frame, width=70, height=70, bg="white", highlightthickness=0)
avatar_canvas.place(x=20, y=20)
avatar_canvas.create_oval(5, 5, 65, 65, fill="#e6f0f8", outline="#bbbbbb")
avatar_canvas.create_text(35, 35, text="👤", font=("Segoe UI", 24))

tk.Label(profile_frame, text="Good Morning,", font=("Segoe UI", 11), bg="white", anchor="w").place(x=100, y=25)
tk.Label(profile_frame, text="Monther", font=("Segoe UI", 14, "bold"), bg="white", anchor="w").place(x=100, y=50)

import calendar

today = datetime.date.today()
days_in_month = calendar.monthrange(today.year, today.month)[1]
remaining_days = days_in_month - today.day + 1
month_name = today.strftime("%B")

# Count weekdays and weekends
weekdays = 0
weekends = 0
for day in range(today.day, days_in_month + 1):
    weekday = datetime.date(today.year, today.month, day).weekday()
    if weekday < 5:
        weekdays += 1
    else:
        weekends += 1

completion_percent = round((today.day - 1) / days_in_month * 100)

tk.Label(profile_frame, text=f"Month: {month_name}", font=("Segoe UI", 10), bg="white").place(x=20, y=100)
tk.Label(profile_frame, text=f"{completion_percent}% Completed", font=("Segoe UI", 9), bg="white").place(x=20, y=125)
tk.Label(profile_frame, text=f"Remaining {remaining_days:02d} Days", font=("Segoe UI", 9), bg="white").place(x=180, y=125)
tk.Label(profile_frame, text=f"• {weekdays:02d} Weekdays", font=("Segoe UI", 9), fg="#000", bg="white").place(x=20, y=150)
tk.Label(profile_frame, text=f"• {weekends:02d} Weekends & Holidays", font=("Segoe UI", 9), fg="green", bg="white").place(x=20, y=170)


# Chart (right)
fig = generate_chart()
if fig:
    chart_canvas = FigureCanvasTkAgg(fig, master=top_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().place(x=500, y=10)

# Category Cards
middle_wrapper = tk.Frame(root, bg="#f5f7fa")
middle_wrapper.pack(fill="both", expand=True, padx=10)

category_frame = tk.Frame(middle_wrapper, bg="#ffffff")
category_frame.grid(row=0, column=0, sticky="n", padx=(0, 20))

def refresh_category_cards():
    for widget in category_frame.winfo_children():
        widget.destroy()

    tk.Label(category_frame, text="Category-wise Expenses", font=("Segoe UI", 14, "bold"), bg="#ffffff").pack(anchor="w", pady=(0, 5))
    cards_container = tk.Frame(category_frame, bg="#ffffff")
    cards_container.pack()

    for idx, (cat, meta) in enumerate(category_data.items()):
        total = get_category_total(cat)
        card = tk.Frame(cards_container, bg=meta["color"], width=180, height=80, bd=1, relief="ridge")
        card.grid(row=idx//4, column=idx%4, padx=5, pady=5)
        tk.Label(card, text=f"{meta['emoji']} {cat}", font=("Segoe UI", 11, "bold"), bg=meta["color"]).pack(pady=5)
        tk.Label(card, text=f"${total:,.2f}", font=("Segoe UI", 10), bg=meta["color"]).pack()

# Activity / Transaction History
activity_frame = tk.Frame(middle_wrapper, bg="#ffffff")
activity_frame.grid(row=0, column=1, sticky="n")

title_row = tk.Frame(activity_frame, bg="#ffffff")
title_row.pack(fill="x", padx=5, pady=(0, 5))

tk.Label(title_row, text="Transaction History", font=("Segoe UI", 14), bg="#ffffff").pack(side="left")
add_button = tk.Button(title_row, text="➕ Add Transaction", command=open_add_transaction,
                       bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"))
add_button.pack(side="right")

search_var = tk.StringVar()
def search_transactions():
    query = search_var.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_transactions():
        if query in str(row).lower():
            tree.insert("", "end", values=row)

search_row = tk.Frame(activity_frame, bg="#ffffff")
search_row.pack(fill="x", padx=5, pady=(0, 10))

search_box = tk.Entry(search_row, textvariable=search_var, width=30, font=("Segoe UI", 10))
search_box.pack(side="left", padx=(0, 8), ipady=3)

search_btn = tk.Button(search_row, text="Search", command=search_transactions, 
                       bg="#2196F3", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=3)
search_btn.pack(side="left")

columns = ("ID", "Date", "Category", "Amount", "Notes")
tree = ttk.Treeview(activity_frame, columns=columns, show="headings", height=7)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)
tree.pack(fill="x", padx=5)

# Upcoming Transactions
tk.Label(activity_frame, text="Upcoming Transactions", font=("Segoe UI", 14), bg="#ffffff").pack(anchor="w", padx=5, pady=(10, 0))

upcoming_data = [
    ("20 Aug", "Door Handle Replacement", "$360", "Cash"),
    ("18 Aug", "Nike Running Shoe", "$150", "Card"),
    ("18 Aug", "Mutual Fund", "$500", "Card")
]

for date, item, price, method in upcoming_data:
    frame = tk.Frame(activity_frame, bg="#f7f7f7", bd=1, relief="solid")
    frame.pack(fill="x", padx=5, pady=2)

    tk.Label(frame, text=f"{date} - {item}", font=("Segoe UI", 10), bg="#f7f7f7", anchor="w").pack(side="left", padx=5)
    tk.Label(frame, text=price, font=("Segoe UI", 10, "bold"), bg="#f7f7f7", fg="#333").pack(side="left", padx=5)
    tag_color = "#4CAF50" if method == "Cash" else "#2196F3"
    tk.Label(frame, text=method, font=("Segoe UI", 9, "bold"), bg=tag_color, fg="white", padx=8).pack(side="right", padx=5)

# Refresh everything
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_transactions():
        tree.insert("", "end", values=row)
    refresh_category_cards()

refresh_table()
root.mainloop()
