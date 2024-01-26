import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        self.length_label = ttk.Label(root, text="Password Length:")
        self.length_entry = ttk.Entry(root)
        self.length_entry.insert(0, "12")  # Default length

        self.upper_var = tk.IntVar()
        self.upper_check = ttk.Checkbutton(root, text="Include Uppercase", variable=self.upper_var)

        self.lower_var = tk.IntVar()
        self.lower_check = ttk.Checkbutton(root, text="Include Lowercase", variable=self.lower_var)

        self.digit_var = tk.IntVar()
        self.digit_check = ttk.Checkbutton(root, text="Include Digits", variable=self.digit_var)

        self.symbol_var = tk.IntVar()
        self.symbol_check = ttk.Checkbutton(root, text="Include Symbols", variable=self.symbol_var)

        self.generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password)
        self.copy_button = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)

        self.result_label = ttk.Label(root, text="Generated Password: ")

        # Grid Layout
        self.length_label.grid(row=0, column=0, pady=5, sticky="w")
        self.length_entry.grid(row=0, column=1, pady=5, sticky="w")
        self.upper_check.grid(row=1, column=0, pady=5, sticky="w")
        self.lower_check.grid(row=2, column=0, pady=5, sticky="w")
        self.digit_check.grid(row=3, column=0, pady=5, sticky="w")
        self.symbol_check.grid(row=4, column=0, pady=5, sticky="w")
        self.generate_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.copy_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.result_label.grid(row=7, column=0, columnspan=2, pady=10)

    def generate_password(self):
        length = int(self.length_entry.get())
        include_upper = bool(self.upper_var.get())
        include_lower = bool(self.lower_var.get())
        include_digit = bool(self.digit_var.get())
        include_symbol = bool(self.symbol_var.get())

        characters = ""
        if include_upper:
            characters += string.ascii_uppercase
        if include_lower:
            characters += string.ascii_lowercase
        if include_digit:
            characters += string.digits
        if include_symbol:
            characters += string.punctuation

        if not any([include_upper, include_lower, include_digit, include_symbol]):
            messagebox.showwarning("Warning", "Select at least one character type.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.result_label["text"] = f"Generated Password: {password}"

    def copy_to_clipboard(self):
        password = self.result_label["text"].split(": ")[1]
        pyperclip.copy(password)
        messagebox.showinfo("Info", "Password copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
