import tkinter as tk
from tkinter import ttk
from math import sqrt, exp, sin, cos, tan, log, sinh, cosh, tanh, pi, e, factorial, radians
import re

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Ilmiah")
        self.root.geometry("500x700")
        self.entry_var = tk.StringVar()
        self.memory = 0
        self.create_widgets()
        self.configure_grid()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14, 'bold'), padding=10, background="#1c1e24", foreground="#3969ed")
        style.configure('TEntry', font=('Arial', 24, 'bold'), padding=10)
        style.configure('TLabel', font=('Arial', 12), padding=10)

        entry = ttk.Entry(self.root, textvariable=self.entry_var, justify='right', width=20, font=('Arial', 24, 'bold'))
        entry.grid(row=0, column=0, columnspan=5, sticky='nsew', padx=10, pady=10)

        history_label = ttk.Label(self.root, text="Riwayat Perhitungan:")
        history_label.grid(row=1, column=0, columnspan=5, sticky='w', padx=10)

        self.history_list = tk.Listbox(self.root, height=10, font=('Arial', 12))
        self.history_list.grid(row=2, column=0, columnspan=5, sticky='nsew', padx=10, pady=10)

        clear_history_btn = ttk.Button(self.root, text="Hapus Riwayat", command=self.clear_history)
        clear_history_btn.grid(row=3, column=0, columnspan=5, sticky='nsew', padx=10, pady=5)

        button_texts = [
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3), ('sqrt', 4, 4),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3), ('exp', 5, 4),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3), ('sin', 6, 4),
            ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('+', 7, 3), ('cos', 7, 4),
            ('C', 8, 0), ('log', 8, 1), ('sinh', 8, 2), ('tan', 8, 3), ('cosh', 8, 4),
            ('pi', 9, 0), ('e', 9, 1), ('tanh', 9, 2), ('(', 9, 3), (')', 9, 4),
            ('!', 10, 0), ('^', 10, 1), ('M+', 10, 2), ('M-', 10, 3), ('MR', 10, 4), ('MC', 11, 0)
        ]

        for (text, row, col) in button_texts:
            if text == '=':
                btn = ttk.Button(self.root, text=text, command=self.evaluate_expression)
            elif text == 'C':
                btn = tk.Button(self.root, text=text, command=self.clear_entry, bg="red", fg="white", font=('Arial', 14, 'bold'))
            elif text == 'M+':
                btn = ttk.Button(self.root, text=text, command=self.memory_add)
            elif text == 'M-':
                btn = ttk.Button(self.root, text=text, command=self.memory_subtract)
            elif text == 'MR':
                btn = ttk.Button(self.root, text=text, command=self.memory_recall)
            elif text == 'MC':
                btn = ttk.Button(self.root, text=text, command=self.memory_clear)
            else:
                btn = ttk.Button(self.root, text=text, command=lambda t=text: self.append_to_expression(t))
            btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

    def configure_grid(self):
        for i in range(5):
            self.root.columnconfigure(i, weight=1)
        for i in range(12):
            self.root.rowconfigure(i, weight=1)

    def evaluate_expression(self):
        expression = self.entry_var.get()
        try:
            expression = self.preprocess_expression(expression)
            result = eval(expression, {"sqrt": sqrt, "exp": exp, "sin": lambda x: sin(radians(x)), "cos": lambda x: cos(radians(x)), "tan": lambda x: tan(radians(x)), "log": log, "sinh": sinh, "cosh": cosh, "tanh": tanh, "pi": pi, "e": e, "factorial": factorial})
            self.entry_var.set(result)
            self.add_to_history(expression + " = " + str(result))
        except Exception as err:
            self.entry_var.set("Error: " + str(err))

    def preprocess_expression(self, expression):
        expression = expression.replace('^', '**')
        expression = re.sub(r'(\d+)!', r'factorial(\1)', expression)
        return expression

    def append_to_expression(self, text):
        current_text = self.entry_var.get()
        new_text = current_text + str(text)
        self.entry_var.set(new_text)

    def clear_entry(self):
        self.entry_var.set("")

    def add_to_history(self, entry):
        self.history_list.insert(tk.END, entry)

    def clear_history(self):
        self.history_list.delete(0, tk.END)

    def memory_add(self):
        try:
            self.memory += float(self.entry_var.get())
        except ValueError:
            self.entry_var.set("Error")

    def memory_subtract(self):
        try:
            self.memory -= float(self.entry_var.get())
        except ValueError:
            self.entry_var.set("Error")

    def memory_recall(self):
        self.entry_var.set(str(self.memory))

    def memory_clear(self):
        self.memory = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
