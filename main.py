import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import init_db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime
import tkinter.font as tkFont

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

    # Modern chart styling
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(5, 3), facecolor='#1e1e1e')
    ax.set_facecolor('#2d2d2d')
    
    # Modern gradient line
    ax.plot(dates, totals, marker='o', linestyle='-', color="#00d4aa", linewidth=3, markersize=6, markerfacecolor="#00d4aa", markeredgecolor="#ffffff", markeredgewidth=1)
    
    ax.set_title("Expenses Over Time", color="#ffffff", fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Date", color="#cccccc", fontsize=11)
    ax.set_ylabel("Total Spent ($)", color="#cccccc", fontsize=11)
    ax.tick_params(axis='x', rotation=45, colors="#cccccc")
    ax.tick_params(axis='y', colors="#cccccc")
    
    # Grid styling
    ax.grid(True, alpha=0.3, color="#444444")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444444')
    ax.spines['bottom'].set_color('#444444')
    
    fig.tight_layout()
    return fig

# Modern category data with updated colors
category_data = {
    "Food": {"emoji": "🍔", "color": "#ff6b6b", "gradient": "#ff8e8e"},
    "Rent": {"emoji": "🏠", "color": "#4ecdc4", "gradient": "#6ed5cd"},
    "Transport": {"emoji": "🚗", "color": "#45b7d1", "gradient": "#5bc0de"},
    "Bills": {"emoji": "💡", "color": "#f9ca24", "gradient": "#fad02e"},
    "Healthcare": {"emoji": "💊", "color": "#6c5ce7", "gradient": "#7b68ee"},
    "Education": {"emoji": "📚", "color": "#a29bfe", "gradient": "#b2a8ff"},
    "Investment": {"emoji": "💰", "color": "#00b894", "gradient": "#00cec9"},
    "Other": {"emoji": "🧾", "color": "#fd79a8", "gradient": "#fdcb6e"}
}

# Modern add transaction form
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
    form.geometry("420x500")
    form.config(bg="#1e1e1e")
    form.resizable(False, False)
    
    # Center the window
    form.transient(root)
    form.grab_set()
    
    # Header
    header_frame = tk.Frame(form, bg="#2d2d2d", height=60)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="➕ Add New Transaction", 
             font=("Segoe UI", 16, "bold"), 
             bg="#2d2d2d", fg="#ffffff").pack(expand=True)
    
    # Main content
    content_frame = tk.Frame(form, bg="#1e1e1e")
    content_frame.pack(fill="both", expand=True, padx=30, pady=20)
    
    # Form fields with modern styling
    def create_field(label_text, widget, row):
        label = tk.Label(content_frame, text=label_text, 
                        font=("Segoe UI", 11, "bold"), 
                        bg="#1e1e1e", fg="#cccccc", anchor="w")
        label.grid(row=row, column=0, sticky="w", pady=(15, 5))
        
        if isinstance(widget, tk.Entry):
            widget.config(font=("Segoe UI", 11), bg="#2d2d2d", fg="#ffffff", 
                         insertbackground="#ffffff", relief="flat", bd=0)
        elif isinstance(widget, ttk.Combobox):
            style = ttk.Style()
            style.configure("Modern.TCombobox", fieldbackground="#2d2d2d", 
                           background="#2d2d2d", foreground="#ffffff", 
                           borderwidth=0, relief="flat")
            widget.config(style="Modern.TCombobox", font=("Segoe UI", 11))
        
        widget.grid(row=row+1, column=0, sticky="ew", pady=(0, 10), ipady=8, ipadx=10)
        content_frame.grid_columnconfigure(0, weight=1)

    # Date field
    date_entry = tk.Entry(content_frame, width=30)
    create_field("📅 Date (YYYY-MM-DD):", date_entry, 0)
    
    # Category field
    category_var = tk.StringVar()
    category_menu = ttk.Combobox(content_frame, textvariable=category_var, 
                                values=list(category_data.keys()), state="readonly")
    create_field("🏷️ Category:", category_menu, 2)
    
    # Amount field
    amount_entry = tk.Entry(content_frame, width=30)
    create_field("💰 Amount ($):", amount_entry, 4)
    
    # Notes field
    notes_entry = tk.Entry(content_frame, width=30)
    create_field("📝 Notes:", notes_entry, 6)
    
    # Payment type field
    payment_type_var = tk.StringVar(value="Cash")
    payment_menu = ttk.Combobox(content_frame, textvariable=payment_type_var, 
                               values=["Cash", "Card"], state="readonly")
    create_field("💳 Payment Type:", payment_menu, 8)
    
    # Upcoming checkbox
    upcoming_var = tk.IntVar()
    checkbox_frame = tk.Frame(content_frame, bg="#1e1e1e")
    checkbox_frame.grid(row=10, column=0, sticky="w", pady=(15, 20))
    
    checkbox = tk.Checkbutton(checkbox_frame, text="🔮 Mark as Upcoming Transaction", 
                             variable=upcoming_var, 
                             font=("Segoe UI", 11), 
                             bg="#1e1e1e", fg="#cccccc", 
                             selectcolor="#2d2d2d", 
                             activebackground="#1e1e1e", 
                             activeforeground="#ffffff")
    checkbox.pack(side="left")
    
    # Submit button
    submit_btn = tk.Button(content_frame, text="✨ Add Transaction", 
                          command=submit, 
                          font=("Segoe UI", 12, "bold"),
                          bg="#00d4aa", fg="#ffffff", 
                          relief="flat", bd=0,
                          padx=30, pady=12,
                          cursor="hand2")
    submit_btn.grid(row=11, column=0, pady=(20, 0))
    
    # Hover effects
    def on_enter(e):
        submit_btn.config(bg="#00b894")
    def on_leave(e):
        submit_btn.config(bg="#00d4aa")
    
    submit_btn.bind("<Enter>", on_enter)
    submit_btn.bind("<Leave>", on_leave)

# Main window with modern styling
root = tk.Tk()
root.title("💰 Finance Tracker - Modern Dashboard")
root.geometry("1200x800")
root.configure(bg="#1e1e1e")
root.minsize(1000, 700)

# Create main frame with scrollbar
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True)

# Create canvas and scrollbar
canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

# Configure scrolling
def configure_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scroll_region)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Make scrollable frame fill the full width
def configure_scrollable_frame(event):
    canvas_width = event.width
    canvas.itemconfig(canvas.find_all()[0], width=canvas_width)

canvas.bind('<Configure>', configure_scrollable_frame)

# Pack canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Mouse wheel binding
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Configure modern fonts
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Segoe UI", size=10)

# Configure ttk styles for modern look
style = ttk.Style()
style.theme_use('clam')
style.configure("Modern.Treeview", 
                background="#2d2d2d", 
                foreground="#ffffff", 
                fieldbackground="#2d2d2d",
                borderwidth=0,
                font=("Segoe UI", 10))
style.configure("Modern.Treeview.Heading", 
                background="#3d3d3d", 
                foreground="#ffffff", 
                font=("Segoe UI", 10, "bold"),
                borderwidth=0)
style.map("Modern.Treeview", 
          background=[('selected', '#00d4aa')])

# ────────────────────────
# 🎨 Modern Top Section
# ────────────────────────
top_frame = tk.Frame(scrollable_frame, bg="#2d2d2d", height=320)
top_frame.pack(fill="x", padx=20, pady=(20, 0))
top_frame.pack_propagate(False)

# Modern header
header_frame = tk.Frame(top_frame, bg="#2d2d2d", height=60)
header_frame.pack(fill="x", padx=20, pady=(20, 0))

tk.Label(header_frame, text="💰 Finance Dashboard", 
         font=("Segoe UI", 24, "bold"), 
         bg="#2d2d2d", fg="#ffffff").pack(side="left")

# Welcome message
import calendar
today = datetime.date.today()
now = datetime.datetime.now()
month_name = today.strftime("%B")
day_name = today.strftime("%A")

tk.Label(header_frame, text=f"Good {('morning' if now.hour < 12 else 'afternoon' if now.hour < 18 else 'evening')}, Monther! • {day_name}, {month_name} {today.day}", 
         font=("Segoe UI", 12), 
         bg="#2d2d2d", fg="#cccccc").pack(side="right")

# Content area
content_top = tk.Frame(top_frame, bg="#2d2d2d")
content_top.pack(fill="both", expand=True, padx=20, pady=20)

# Profile card (left)
profile_frame = tk.Frame(content_top, bg="#3d3d3d", width=350, height=200, relief="flat", bd=0)
profile_frame.pack(side="left", padx=(0, 20))
profile_frame.pack_propagate(False)

# Profile header
profile_header = tk.Frame(profile_frame, bg="#4d4d4d", height=50)
profile_header.pack(fill="x")
profile_header.pack_propagate(False)

tk.Label(profile_header, text="👤 Profile Overview", 
         font=("Segoe UI", 14, "bold"), 
         bg="#4d4d4d", fg="#ffffff").pack(expand=True)

# Profile content
profile_content = tk.Frame(profile_frame, bg="#3d3d3d")
profile_content.pack(fill="both", expand=True, padx=20, pady=15)

# Month progress
days_in_month = calendar.monthrange(today.year, today.month)[1]
remaining_days = days_in_month - today.day + 1
completion_percent = round((today.day - 1) / days_in_month * 100)

tk.Label(profile_content, text=f"📅 {month_name} Progress", 
         font=("Segoe UI", 12, "bold"), 
         bg="#3d3d3d", fg="#ffffff", anchor="w").pack(anchor="w", pady=(0, 5))

# Progress bar
progress_frame = tk.Frame(profile_content, bg="#2d2d2d", height=8, relief="flat")
progress_frame.pack(fill="x", pady=(0, 10))
progress_frame.pack_propagate(False)

progress_fill = tk.Frame(progress_frame, bg="#00d4aa", width=int(progress_frame.winfo_reqwidth() * completion_percent / 100))
progress_fill.pack(side="left", fill="y")

tk.Label(profile_content, text=f"{completion_percent}% Complete • {remaining_days} days remaining", 
         font=("Segoe UI", 10), 
         bg="#3d3d3d", fg="#cccccc").pack(anchor="w")

# Stats
stats_frame = tk.Frame(profile_content, bg="#3d3d3d")
stats_frame.pack(fill="x", pady=(15, 0))

# Count weekdays and weekends
weekdays = 0
weekends = 0
for day in range(today.day, days_in_month + 1):
    weekday = datetime.date(today.year, today.month, day).weekday()
    if weekday < 5:
        weekdays += 1
    else:
        weekends += 1

tk.Label(stats_frame, text=f"📊 {weekdays} weekdays • 🏖️ {weekends} weekends", 
         font=("Segoe UI", 10), 
         bg="#3d3d3d", fg="#cccccc").pack(anchor="w")

# Chart (right)
chart_frame = tk.Frame(content_top, bg="#3d3d3d", relief="flat", bd=0)
chart_frame.pack(side="right", fill="both", expand=True)

# Chart header
chart_header = tk.Frame(chart_frame, bg="#4d4d4d", height=50)
chart_header.pack(fill="x")
chart_header.pack_propagate(False)

tk.Label(chart_header, text="📈 Spending Trends", 
         font=("Segoe UI", 14, "bold"), 
         bg="#4d4d4d", fg="#ffffff").pack(expand=True)

# Chart content
chart_content = tk.Frame(chart_frame, bg="#3d3d3d")
chart_content.pack(fill="both", expand=True, padx=10, pady=10)

fig = generate_chart()
if fig:
    chart_canvas = FigureCanvasTkAgg(fig, master=chart_content)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(fill="both", expand=True)
else:
    tk.Label(chart_content, text="📊 No data available\nAdd some transactions to see trends!", 
             font=("Segoe UI", 12), 
             bg="#3d3d3d", fg="#888888", 
             justify="center").pack(expand=True)

# ────────────────────────
# 🎨 Modern Middle Section
# ────────────────────────
middle_wrapper = tk.Frame(scrollable_frame, bg="#1e1e1e")
middle_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

# Left side - Category Cards
category_frame = tk.Frame(middle_wrapper, bg="#2d2d2d", relief="flat", bd=0)
category_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

def refresh_category_cards():
    for widget in category_frame.winfo_children():
        widget.destroy()

    # Category header
    category_header = tk.Frame(category_frame, bg="#3d3d3d", height=50)
    category_header.pack(fill="x")
    category_header.pack_propagate(False)
    
    tk.Label(category_header, text="🏷️ Category Breakdown", 
             font=("Segoe UI", 16, "bold"), 
             bg="#3d3d3d", fg="#ffffff").pack(expand=True)

    # Cards container
    cards_container = tk.Frame(category_frame, bg="#2d2d2d")
    cards_container.pack(fill="both", expand=True, padx=15, pady=15)

    for idx, (cat, meta) in enumerate(category_data.items()):
        total = get_category_total(cat)
        
        # Modern card design
        card = tk.Frame(cards_container, bg="#3d3d3d", relief="flat", bd=0)
        card.grid(row=idx//2, column=idx%2, padx=8, pady=8, sticky="ew")
        cards_container.grid_columnconfigure(idx%2, weight=1)
        
        # Card content
        card_content = tk.Frame(card, bg=meta["color"], relief="flat", bd=0)
        card_content.pack(fill="both", expand=True, padx=15, pady=12)
        
        # Category name and emoji
        name_frame = tk.Frame(card_content, bg=meta["color"])
        name_frame.pack(fill="x", pady=(0, 8))
        
        tk.Label(name_frame, text=meta['emoji'], 
                font=("Segoe UI", 16), 
                bg=meta["color"]).pack(side="left")
        
        tk.Label(name_frame, text=cat, 
                font=("Segoe UI", 12, "bold"), 
                bg=meta["color"], fg="#2d2d2d").pack(side="left", padx=(8, 0))
        
        # Amount
        tk.Label(card_content, text=f"${total:,.2f}", 
                font=("Segoe UI", 14, "bold"), 
                bg=meta["color"], fg="#1a1a1a").pack(anchor="w")
        
        # Percentage indicator (if there are transactions)
        if total > 0:
            tk.Label(card_content, text="●", 
                    font=("Segoe UI", 8), 
                    bg=meta["color"], fg="#00d4aa").pack(anchor="w", pady=(2, 0))

# Right side - Transaction History
activity_frame = tk.Frame(middle_wrapper, bg="#2d2d2d", relief="flat", bd=0)
activity_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

# Transaction header
transaction_header = tk.Frame(activity_frame, bg="#3d3d3d", height=50)
transaction_header.pack(fill="x")
transaction_header.pack_propagate(False)

tk.Label(transaction_header, text="📋 Transaction History", 
         font=("Segoe UI", 16, "bold"), 
         bg="#3d3d3d", fg="#ffffff").pack(side="left", padx=15, expand=True)

# Add transaction button
add_button = tk.Button(transaction_header, text="➕ Add Transaction", 
                       command=open_add_transaction,
                       bg="#00d4aa", fg="#ffffff", 
                       font=("Segoe UI", 11, "bold"),
                       relief="flat", bd=0,
                       padx=15, pady=8,
                       cursor="hand2")
add_button.pack(side="right", padx=15)

# Search section
search_frame = tk.Frame(activity_frame, bg="#2d2d2d")
search_frame.pack(fill="x", padx=15, pady=15)

search_var = tk.StringVar()
def search_transactions():
    query = search_var.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_transactions():
        if query in str(row).lower():
            tree.insert("", "end", values=row)

# Modern search box
search_container = tk.Frame(search_frame, bg="#3d3d3d", relief="flat", bd=0)
search_container.pack(fill="x")

search_box = tk.Entry(search_container, textvariable=search_var, 
                     font=("Segoe UI", 11), 
                     bg="#2d2d2d", fg="#ffffff", 
                     insertbackground="#ffffff", 
                     relief="flat", bd=0)
search_box.pack(side="left", fill="x", expand=True, ipady=10, ipadx=15)

search_btn = tk.Button(search_container, text="🔍", 
                       command=search_transactions, 
                       bg="#4d4d4d", fg="#ffffff", 
                       font=("Segoe UI", 12),
                       relief="flat", bd=0,
                       padx=15, pady=10,
                       cursor="hand2")
search_btn.pack(side="right")

# Transaction table
table_frame = tk.Frame(activity_frame, bg="#2d2d2d")
table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

columns = ("Date", "Category", "Amount", "Notes")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8, style="Modern.Treeview")
for col in columns:
    tree.heading(col, text=col)
    if col == "Amount":
        tree.column(col, anchor="e", width=100)
    elif col == "Date":
        tree.column(col, anchor="center", width=100)
    else:
        tree.column(col, anchor="w", width=120)

# Scrollbar for table
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Upcoming Transactions Section
upcoming_frame = tk.Frame(activity_frame, bg="#2d2d2d")
upcoming_frame.pack(fill="x", padx=15, pady=(15, 0))

upcoming_header = tk.Frame(upcoming_frame, bg="#3d3d3d", height=40)
upcoming_header.pack(fill="x")
upcoming_header.pack_propagate(False)

tk.Label(upcoming_header, text="🔮 Upcoming Transactions", 
         font=("Segoe UI", 12, "bold"), 
         bg="#3d3d3d", fg="#ffffff").pack(expand=True)

# Upcoming transactions list
upcoming_data = [
    ("20 Aug", "Door Handle Replacement", "$360", "Cash"),
    ("18 Aug", "Nike Running Shoe", "$150", "Card"),
    ("18 Aug", "Mutual Fund", "$500", "Card")
]

upcoming_list = tk.Frame(upcoming_frame, bg="#2d2d2d")
upcoming_list.pack(fill="x", pady=(10, 0))

for date, item, price, method in upcoming_data:
    transaction_item = tk.Frame(upcoming_list, bg="#3d3d3d", relief="flat", bd=0)
    transaction_item.pack(fill="x", pady=3)
    
    # Left side - date and item
    left_frame = tk.Frame(transaction_item, bg="#3d3d3d")
    left_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)
    
    tk.Label(left_frame, text=f"📅 {date}", 
             font=("Segoe UI", 9, "bold"), 
             bg="#3d3d3d", fg="#00d4aa").pack(anchor="w")
    
    tk.Label(left_frame, text=item, 
             font=("Segoe UI", 10), 
             bg="#3d3d3d", fg="#ffffff").pack(anchor="w")
    
    # Right side - price and method
    right_frame = tk.Frame(transaction_item, bg="#3d3d3d")
    right_frame.pack(side="right", padx=10, pady=8)
    
    tk.Label(right_frame, text=price, 
             font=("Segoe UI", 11, "bold"), 
             bg="#3d3d3d", fg="#ffffff").pack(anchor="e")
    
    tag_color = "#00d4aa" if method == "Cash" else "#4d4d4d"
    tk.Label(right_frame, text=method, 
             font=("Segoe UI", 9, "bold"), 
             bg=tag_color, fg="#ffffff", 
             padx=8, pady=2).pack(anchor="e", pady=(2, 0))

# Refresh everything
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_transactions():
        # Format the row data (remove ID column for display)
        display_row = row[1:]  # Skip ID column
        tree.insert("", "end", values=display_row)
    refresh_category_cards()
    # Update scroll region after content changes
    root.after(50, configure_scroll_region)

# Add hover effects for buttons
def add_hover_effects():
    def on_enter_add(e):
        add_button.config(bg="#00b894")
    def on_leave_add(e):
        add_button.config(bg="#00d4aa")
    
    add_button.bind("<Enter>", on_enter_add)
    add_button.bind("<Leave>", on_leave_add)
    
    def on_enter_search(e):
        search_btn.config(bg="#5d5d5d")
    def on_leave_search(e):
        search_btn.config(bg="#4d4d4d")
    
    search_btn.bind("<Enter>", on_enter_search)
    search_btn.bind("<Leave>", on_leave_search)

# Initialize the application
refresh_table()
add_hover_effects()

# Update scroll region after everything is loaded
root.after(100, configure_scroll_region)

# Add some final styling touches
root.configure(highlightthickness=0)

# Start the application
root.mainloop()
