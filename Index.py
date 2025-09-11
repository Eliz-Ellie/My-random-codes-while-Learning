import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to a database (or create it)
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Insert a row of data (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
	cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
	conn.commit()

# --- Helper functions ---
def refresh_table():
	for row in tree.get_children():
		tree.delete(row)
	conn = sqlite3.connect('mydatabase.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users")
	for row in cursor.fetchall():
		tree.insert("", tk.END, values=row)
	conn.close()

def add_user():
	name = name_entry.get()
	try:
		age = int(age_entry.get())
	except ValueError:
		return  # Ignore invalid age
	if name:
		conn = sqlite3.connect('mydatabase.db')
		cursor = conn.cursor()
		cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
		conn.commit()
		conn.close()
		refresh_table()
		name_entry.delete(0, tk.END)
		age_entry.delete(0, tk.END)

def remove_user():
	selected = tree.selection()
	if selected:
		user_id = tree.item(selected[0])['values'][0]
		conn = sqlite3.connect('mydatabase.db')
		cursor = conn.cursor()
		cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
		conn.commit()
		conn.close()
		refresh_table()

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Users in Database")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tree = ttk.Treeview(frame, columns=("ID", "Name", "Age"), show="headings", height=8)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

form_frame = tk.Frame(frame)
form_frame.pack(fill=tk.X, pady=5)

tk.Label(form_frame, text="Name:").pack(side=tk.LEFT)
name_entry = tk.Entry(form_frame)
name_entry.pack(side=tk.LEFT, padx=5)

tk.Label(form_frame, text="Age:").pack(side=tk.LEFT)
age_entry = tk.Entry(form_frame, width=5)
age_entry.pack(side=tk.LEFT, padx=5)

add_btn = tk.Button(form_frame, text="Add User", command=add_user)
add_btn.pack(side=tk.LEFT, padx=5)

remove_btn = tk.Button(form_frame, text="Remove Selected", command=remove_user)
remove_btn.pack(side=tk.LEFT, padx=5)

refresh_table()

root.mainloop()