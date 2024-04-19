from cryptography.fernet import Fernet
import sqlite3
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, Toplevel, Button, ttk
from datetime import datetime


class DiaryApp:
    def __init__(self, master, password):
        self.master = master
        master.title("Personal Diary System")

        # Load the encryption key
        with open("../secret.key", "rb") as key_file:
            key = key_file.read()
        self.cipher_suite = Fernet(key)

        # Check password at startup
        password_input = simpledialog.askstring("Password", "Enter your password:", show='*')
        if password_input != password:
            messagebox.showerror("Error", "Incorrect password!")
            master.destroy()
            return

        # Initialize the rest of the GUI
        self.text_area = scrolledtext.ScrolledText(master, width=40, height=20)
        self.text_area.pack(pady=20)
        self.save_button = Button(master, text="Save Entry", command=self.save_entry)
        self.save_button.pack(side=tk.LEFT, padx=10)
        self.view_button = Button(master, text="View Past Entries", command=self.view_entries)
        self.view_button.pack(side=tk.RIGHT, padx=10)

    def save_entry(self):
        entry = self.text_area.get("1.0", "end-1c")
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        if entry.strip():
            encrypted_entry = self.cipher_suite.encrypt(entry.encode('utf-8'))
            self.insert_entry(date, time, encrypted_entry)
            messagebox.showinfo("Saved", "Your entry has been saved at {} on {}.".format(time, date))
            self.text_area.delete("1.0", "end")

    def insert_entry(self, date, time, entry):
        conn = sqlite3.connect('diary2.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (date, time, entry) VALUES (?, ?, ?)", (date, time, entry))
        conn.commit()
        conn.close()

    def view_entries(self):
        view_window = Toplevel(self.master)
        view_window.title("Past Diary Entries")

        tree = ttk.Treeview(view_window, columns=('Date', 'Time', 'Entry'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Entry', text='Entry (Preview)')
        tree.column('Date', width=100)
        tree.column('Time', width=100)
        tree.column('Entry', width=300)

        scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)

        conn = sqlite3.connect('diary2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT date, time, entry FROM entries")
        rows = cursor.fetchall()
        for row in rows:
            try:
                full_entry = self.cipher_suite.decrypt(row[2]).decode('utf-8')
                entry_preview = (full_entry[:20] + '...') if len(full_entry) > 20 else full_entry
            except Exception as e:
                full_entry = "Error decrypting entry: {}".format(e)
                entry_preview = full_entry
            tree.insert('', 'end', values=(row[0], row[1], entry_preview))

        # Bind the select event to a new function that will show the entry
        tree.bind("<<TreeviewSelect>>", lambda event: self.show_entry(event, tree, rows))

        conn.close()

    def show_entry(self, event, tree, rows):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            index = tree.index(selected_item)  # Get the index of the selected item
            full_entry = self.cipher_suite.decrypt(rows[index][2]).decode('utf-8')  # Decrypt using the row index
            messagebox.showinfo("Detailed Entry View", full_entry)


root = tk.Tk()
app = DiaryApp(root, password="")  # Replace "YourPasswordHere" with your chosen password
root.mainloop()
