import customtkinter

class InstallationPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Main title
        label = customtkinter.CTkLabel(self, text="Instalaltion", font=("Arial", 32))
        label.grid(row=0, column=0, columnspan=2, pady=20, padx=60, sticky="nsew")

        # Subtitle 'Installation'
        installation_title = customtkinter.CTkLabel(self, text="Installation", font=("Arial", 28, "bold"))
        installation_title.grid(row=1, column=0, columnspan=2, pady=(30, 5))

        # Dynamic values
        self.location_value = customtkinter.StringVar(value="Amsterdam")
        self.active_since_value = customtkinter.StringVar(value="01/01/2022")
        self.qanteon_channels_value = customtkinter.StringVar(value="52")

        # Installation key-value pairs
        self.add_key_value_pair("Location:", self.location_value, 2)
        self.add_key_value_pair("Active Since:", self.active_since_value, 3)
        self.add_key_value_pair("Qanteon Channels:", self.qanteon_channels_value, 4)

        # Subtitle 'Provider'
        provider_title = customtkinter.CTkLabel(self, text="Provider", font=("Arial", 28, "bold"))
        provider_title.grid(row=5, column=0, columnspan=2, pady=(30, 5))

        # Dynamic values for provider
        self.remote_datapoints_value = customtkinter.StringVar(value="10")
        self.remote_channels_value = customtkinter.StringVar(value="3")
        self.active_channels_value = customtkinter.StringVar(value="8")

        # Provider key-value pairs
        self.add_key_value_pair("Remote Datapoints:", self.remote_datapoints_value, 6)
        self.add_key_value_pair("Remote Channels:", self.remote_channels_value, 7)
        self.add_key_value_pair("Active Channels:", self.active_channels_value, 8)

    def add_key_value_pair(self, key, value_var, row):
        key_label = customtkinter.CTkLabel(self, text=key, anchor="w", font=("Arial", 18, "bold"))
        key_label.grid(row=row, column=0, padx=20, pady=4, sticky="w")

        value_label = customtkinter.CTkLabel(self, textvariable=value_var, anchor="w", font=("Arial", 18))
        value_label.grid(row=row, column=1, padx=20, pady=4, sticky="w")

    # Methods to update values dynamically
    def update_location(self, new_value):
        self.location_value.set(new_value)

    def update_active_since(self, new_value):
        self.active_since_value.set(new_value)

    def update_qanteon_channels(self, new_value):
        self.qanteon_channels_value.set(new_value)

    def update_remote_datapoints(self, new_value):
        self.remote_datapoints_value.set(new_value)

    def update_remote_channels(self, new_value):
        self.remote_channels_value.set(new_value)

    def update_active_channels(self, new_value):
        self.active_channels_value.set(new_value)