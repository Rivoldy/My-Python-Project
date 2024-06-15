import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, scrolledtext
import sqlite3

# Setup dan konfigurasi database
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()

# Fungsi untuk login atau registrasi
def login_or_register():
    login_window = tk.Toplevel(root)
    login_window.title("Login or Register")
    login_window.geometry("300x200")
    login_window.configure(bg="#f0f0f0")

    tk.Label(login_window, text="Username:", bg="#f0f0f0").grid(row=0, column=0, pady=10, padx=10)
    username_entry = tk.Entry(login_window, width=25)
    username_entry.grid(row=0, column=1, padx=10)

    tk.Label(login_window, text="Password:", bg="#f0f0f0").grid(row=1, column=0, pady=10, padx=10)
    password_entry = tk.Entry(login_window, show='*', width=25)
    password_entry.grid(row=1, column=1, padx=10)

    def verify_login():
        user = username_entry.get()
        pwd = password_entry.get()
        c.execute('SELECT id FROM users WHERE username=? AND password=?', (user, pwd))
        user_id = c.fetchone()
        if user_id:
            login_window.destroy()  # Menutup jendela login jika login sukses
            manage_passwords(user, user_id[0])
        else:
            response = messagebox.askyesno("User Not Found", "Do you want to register?")
            if response:
                c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user, pwd))
                conn.commit()
                user_id = c.lastrowid
                login_window.destroy()  # Menutup jendela login jika registrasi sukses
                manage_passwords(user, user_id)

    tk.Button(login_window, text="Login", command=verify_login, width=10).grid(row=2, columnspan=2, pady=10)

# Fungsi utama untuk mengelola password
def manage_passwords(username, user_id):
    password_window = tk.Toplevel(root)
    password_window.title(f"Password Manager - {username}")
    password_window.geometry("400x300")
    password_window.configure(bg="#f0f0f0")

    passwords_list = tk.Listbox(password_window, height=10)
    passwords_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def refresh_password_list():
        passwords_list.delete(0, tk.END)
        c.execute('SELECT id, website, username FROM passwords WHERE user_id=?', (user_id,))
        for row in c.fetchall():
            passwords_list.insert(tk.END, f"{row[0]}: {row[1]} ({row[2]})")

    def add_password():
        add_window = tk.Toplevel(password_window)
        add_window.title("Add New Password")
        add_window.geometry("300x200")
        add_window.configure(bg="#f0f0f0")

        tk.Label(add_window, text="Website:", bg="#f0f0f0").grid(row=0, column=0, pady=10)
        website = tk.Entry(add_window, width=25)
        website.grid(row=0, column=1)

        tk.Label(add_window, text="Username:", bg="#f0f0f0").grid(row=1, column=0, pady=10)
        usrname = tk.Entry(add_window, width=25)
        usrname.grid(row=1, column=1)

        tk.Label(add_window, text="Password:", bg="#f0f0f0").grid(row=2, column=0, pady=10)
        pwd_entry = tk.Entry(add_window, width=25)
        pwd_entry.grid(row=2, column=1)

        tk.Button(add_window, text="Save", command=lambda: save_password(website.get(), usrname.get(), pwd_entry.get())).grid(row=3, columnspan=2, pady=10)

        def save_password(website, usrname, pwd):
            c.execute('INSERT INTO passwords (website, username, password, user_id) VALUES (?, ?, ?, ?)', (website, usrname, pwd, user_id))
            conn.commit()
            add_window.destroy()
            refresh_password_list()

    def view_or_edit_password():
        selected = passwords_list.get(passwords_list.curselection())
        password_id = selected.split(':')[0]
        edit_window = tk.Toplevel(password_window)
        edit_window.title("View/Edit Password")
        edit_window.geometry("300x200")
        edit_window.configure(bg="#f0f0f0")

        c.execute('SELECT website, username, password FROM passwords WHERE id=?', (password_id,))
        data = c.fetchone()

        tk.Label(edit_window, text="Website:", bg="#f0f0f0").grid(row=0, column=0, pady=10)
        website = tk.Entry(edit_window, width=25)
        website.grid(row=0, column=1)
        website.insert(0, data[0])

        tk.Label(edit_window, text="Username:", bg="#f0f0f0").grid(row=1, column=0, pady=10)
        usrname = tk.Entry(edit_window, width=25)
        usrname.grid(row=1, column=1)
        usrname.insert(0, data[1])

        tk.Label(edit_window, text="Password:", bg="#f0f0f0").grid(row=2, column=0, pady=10)
        pwd_entry = tk.Entry(edit_window, width=25)
        pwd_entry.grid(row=2, column=1)
        pwd_entry.insert(0, data[2])

        tk.Button(edit_window, text="Save Changes", command=lambda: save_edits(password_id, website.get(), usrname.get(), pwd_entry.get())).grid(row=3, column=0, pady=10)
        tk.Button(edit_window, text="Delete Password", command=lambda: delete_password(password_id)).grid(row=3, column=1, pady=10)

        def save_edits(password_id, website, usrname, pwd):
            c.execute('UPDATE passwords SET website=?, username=?, password=? WHERE id=?', (website, usrname, pwd, password_id))
            conn.commit()
            edit_window.destroy()
            refresh_password_list()

        def delete_password(password_id):
            c.execute('DELETE FROM passwords WHERE id=?', (password_id,))
            conn.commit()
            edit_window.destroy()
            refresh_password_list()

    refresh_password_list()
    tk.Button(password_window, text="Add Password", command=add_password).pack(fill=tk.X, padx=10, pady=5)
    tk.Button(password_window, text="View/Edit Selected Password", command=view_or_edit_password).pack(fill=tk.X, padx=10, pady=5)

root = tk.Tk()
root.title("Password Manager")
root.geometry("300x100")
root.configure(bg="#f0f0f0")
tk.Button(root, text="Login/Register", command=login_or_register, width=20).pack(expand=True, padx=20, pady=20)
root.mainloop()
