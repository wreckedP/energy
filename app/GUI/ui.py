import tkinter
import customtkinter
from screens import screens

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Energy Collection System")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Kieback & Peter", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_installation = customtkinter.CTkButton(self.sidebar_frame, text="Installation", command=lambda: self.show_frame(screens["InstallationPage"]))
        self.sidebar_button_installation.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_dataPoints = customtkinter.CTkButton(self.sidebar_frame, text="DataPoints", command=lambda: self.show_frame(screens["DataPointsPage"]))
        self.sidebar_button_dataPoints.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_settings = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=lambda: self.show_frame(screens["SettingsPage"]))
        self.sidebar_button_settings.grid(row=6, column=0, padx=20, pady=10)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main frame for displaying pages
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # dictionary to keep references to the pages
        self.frames = {}

        # Initialize pages
        self.frames = {}
        for page_name, F in screens.items():
            frame = F(parent=self.main_frame, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(screens["InstallationPage"])

    def show_frame(self, page_class):
        page_name = page_class.__name__
        frame = self.frames[page_name]
        frame.tkraise()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()
