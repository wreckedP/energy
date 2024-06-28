import customtkinter

class EditableRow(customtkinter.CTkFrame):
    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.parent = parent

        # Name label
        self.name_label = customtkinter.CTkLabel(self, text=name, anchor="w", font=("Arial", 16))
        self.name_label.pack(padx=10, pady=2)

        # Value entry
        self.value_entry = customtkinter.CTkEntry(self, font=("Arial", 16))
        self.value_entry.insert(0, value)
        self.value_entry.pack(padx=10, pady=2)

    def get_value(self):
        return self.value_entry.get()

    def set_value(self, value):
        self.value_entry.delete(0, "end")
        self.value_entry.insert(0, value)


class CollapsibleRow(customtkinter.CTkFrame):
    def __init__(self, parent, title, details):
        super().__init__(parent)
        self.parent = parent
        self.details = details
        self.is_collapsed = True

        # Button to toggle the collapse
        self.button = customtkinter.CTkButton(self, text=title, command=self.toggle)
        self.button.pack(fill="x", padx=10, pady=5)

        # Frame to hold the details
        self.details_frame = customtkinter.CTkFrame(self)
        self.details_frame.pack(fill="x", padx=10, pady=5)

        # Populate the details frame with the provided details
        self.detail_rows = []
        for detail in details:
            name = detail["name"]
            value = detail["value"]
            row = EditableRow(self.details_frame, name, value)
            row.pack(fill="x", padx=10, pady=2)
            self.detail_rows.append(row)

        # Save button and status label
        self.save_button = customtkinter.CTkButton(self.details_frame, text="Save", command=self.save)
        self.save_button.pack(side="left", padx=10, pady=10)

        self.status_label = customtkinter.CTkLabel(self.details_frame, text="")
        self.status_label.pack(side="left", padx=10, pady=10)

        # Initially hide the details frame
        self.details_frame.pack_forget()

    def toggle(self):
        if self.is_collapsed:
            self.details_frame.pack(fill="x", padx=10, pady=5)
        else:
            self.details_frame.pack_forget()
        self.is_collapsed = not self.is_collapsed

    def get_details(self):
        return {row.name_label.cget("text"): row.get_value() for row in self.detail_rows}

    def save(self):
        # Save the current values and update the status label
        details = self.get_details()
        # You can add saving logic here (e.g., saving to a file or database)
        self.status_label.configure(text="Saved", text_color="green")


class DataPointsPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Main title
        label = customtkinter.CTkLabel(self, text="DataPoints", font=("Arial", 32))
        label.pack(pady=20, padx=60)

        # Scrollable frame for the collapsible rows
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Example collapsible rows
        datapoints = [
            {"title": "Datapoint 1", "details": [{"name": "Detail 1A", "value": "Value 1A"}, {"name": "Detail 1B", "value": "Value 1B"}, {"name": "Detail 1C", "value": "Value 1C"}]},
            {"title": "Datapoint 2", "details": [{"name": "Detail 2A", "value": "Value 2A"}, {"name": "Detail 2B", "value": "Value 2B"}]},
            {"title": "Datapoint 3", "details": [{"name": "Detail 3A", "value": "Value 3A"}, {"name": "Detail 3B", "value": "Value 3B"}, {"name": "Detail 3C", "value": "Value 3C"}, {"name": "Detail 3D", "value": "Value 3D"}]},
            {"title": "Datapoint 1", "details": [{"name": "Detail 1A", "value": "Value 1A"}, {"name": "Detail 1B", "value": "Value 1B"}, {"name": "Detail 1C", "value": "Value 1C"}]},
            {"title": "Datapoint 2", "details": [{"name": "Detail 2A", "value": "Value 2A"}, {"name": "Detail 2B", "value": "Value 2B"}]},
            {"title": "Datapoint 3", "details": [{"name": "Detail 3A", "value": "Value 3A"}, {"name": "Detail 3B", "value": "Value 3B"}, {"name": "Detail 3C", "value": "Value 3C"}, {"name": "Detail 3D", "value": "Value 3D"}]},
            {"title": "Datapoint 1", "details": [{"name": "Detail 1A", "value": "Value 1A"}, {"name": "Detail 1B", "value": "Value 1B"}, {"name": "Detail 1C", "value": "Value 1C"}]},
            {"title": "Datapoint 2", "details": [{"name": "Detail 2A", "value": "Value 2A"}, {"name": "Detail 2B", "value": "Value 2B"}]},
            {"title": "Datapoint 3", "details": [{"name": "Detail 3A", "value": "Value 3A"}, {"name": "Detail 3B", "value": "Value 3B"}, {"name": "Detail 3C", "value": "Value 3C"}, {"name": "Detail 3D", "value": "Value 3D"}]},
            {"title": "Datapoint 1", "details": [{"name": "Detail 1A", "value": "Value 1A"}, {"name": "Detail 1B", "value": "Value 1B"}, {"name": "Detail 1C", "value": "Value 1C"}]},
            {"title": "Datapoint 2", "details": [{"name": "Detail 2A", "value": "Value 2A"}, {"name": "Detail 2B", "value": "Value 2B"}]},
            {"title": "Datapoint 3", "details": [{"name": "Detail 3A", "value": "Value 3A"}, {"name": "Detail 3B", "value": "Value 3B"}, {"name": "Detail 3C", "value": "Value 3C"}, {"name": "Detail 3D", "value": "Value 3D"}]},
        ]

        self.collapsible_rows = []
        for i, datapoint in enumerate(datapoints):
            row = CollapsibleRow(self.scrollable_frame, datapoint["title"], datapoint["details"])
            row.pack(fill="x", padx=10, pady=5)
            self.collapsible_rows.append(row)

    def get_all_details(self):
        return {row.button.cget("text"): row.get_details() for row in self.collapsible_rows}
