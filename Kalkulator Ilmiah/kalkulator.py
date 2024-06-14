import tkinter as tk
from tkinter import ttk
from math import sqrt, exp, sin, cos, tan, log, sinh, cosh, tanh, pi

def evaluate_expression(expression):
    try:
        result = eval(expression, {"sqrt": sqrt, "exp": exp, "sin": sin, "cos": cos, "tan": tan, "log": log, "sinh": sinh, "cosh": cosh, "tanh": tanh, "pi": pi, "e": exp(1)})
        entry_var.set(result)
    except Exception as err:
        entry_var.set("Error: " + str(err))

def append_to_expression(text):
    current_text = entry_var.get()
    new_text = current_text + str(text)
    entry_var.set(new_text)

def clear_entry():
    entry_var.set("")

# Membuat jendela utama
root = tk.Tk()
root.title("Kalkulator Ilmiah")
root.geometry("400x600")  # Menetapkan ukuran jendela

# Styling
style = ttk.Style()
style.configure('TButton', font=('Arial', 14, 'bold'), padding=10, background="#1c1e24", foreground="#3969ed")
style.configure('TEntry', font=('Arial', 24, 'bold'), padding=10)

# Variabel untuk teks entry
entry_var = tk.StringVar()

# Entry widget
entry = ttk.Entry(root, textvariable=entry_var, justify='right', width=20)
entry.grid(row=0, column=0, columnspan=5, sticky='nsew', padx=10, pady=10)

# Buttons
button_texts = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sqrt', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('exp', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('sin', 3, 4),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('cos', 4, 4),
    ('C', 5, 0), ('log', 5, 1), ('sinh', 5, 2), ('tan', 5, 3), ('cosh', 5, 4),
    ('pi', 6, 0), ('e', 6, 1), ('tanh', 6, 2), ('(', 6, 3), (')', 6, 4)
]

for (text, row, col) in button_texts:
    if text == '=':
        btn = ttk.Button(root, text=text, command=lambda: evaluate_expression(entry_var.get()))
    else:
        btn = ttk.Button(root, text=text, command=lambda t=text: append_to_expression(t))
    btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

# Configure grid scaling
for i in range(5):
    root.columnconfigure(i, weight=1)
for i in range(7):
    root.rowconfigure(i, weight=1)

root.mainloop()
