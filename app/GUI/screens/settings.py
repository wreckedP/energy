import customtkinter as ctk
import tkinter as tk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title label
        label = ctk.CTkLabel(self, text="Settings", font=("Arial", 32))
        label.grid(row=0, column=0, columnspan=2, pady=20, padx=60, sticky="nsew")
        
        # Entry fields for each variable
        self.entries = {}

        settings = [
            ("DB_HOST", "<SYSTEM_Geratename>,62522"),
            ("DB_DATABASE", "fenergy"),
            ("DB_USERNAME", ""),
            ("DB_PASSWORD", ""),
            ("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
            ("DB_ENCRYPT", "no"),
            ("USER_USERNAME", "<USERNAME>"),
            ("USER_PASSWORD", "<PASSWORD>")
        ]

        for i, setting in enumerate(settings, start=1):
            name, value = setting
            self.create_setting_entry(i, name, value)

        # Save button
        save_button = ctk.CTkButton(self, text="Save", command=self.save_settings)
        save_button.grid(row=len(settings) + 1, column=0, columnspan=2, pady=20)

    def create_setting_entry(self, row, name, value):
        label = ctk.CTkLabel(self, text=name, anchor="w", font=("Arial", 16))
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        entry = ctk.CTkEntry(self, font=("Arial", 16))
        entry.insert(0, value)
        entry.grid(row=row, column=1, columnspan=3 , padx=10, pady=5, sticky="ew")

        self.entries[name] = entry

    def save_settings(self):
        settings = {name: entry.get() for name, entry in self.entries.items()}
        # You can add saving logic here (e.g., saving to a file or database)
        print(settings)
