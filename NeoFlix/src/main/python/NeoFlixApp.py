import customtkinter as ctk

from src.main.python.Settings import Settings
from src.main.python.frames.FilterFrame import FilterFrame
from src.main.python.frames.MainFrame import MainFrame
from src.main.python.frames.SettingsFrame import SettingsFrame


class NeoFlixApp:
    def __init__(self, app):
        self.app = app
        self.app.title("NeoFlix")
        self.app.geometry("800x600")
        self.app.configure(bg="black")
        self.app.resizable(False, False)
        self.app.iconbitmap("../resources/favicon.ico")
        self.initialize()
        self.app.mainloop()

    def initialize(self):
        self.tab = ctk.CTkTabview(self.app)
        self.tab.pack(fill="both", expand=True)
        self.main_frame =self.tab.add("Main")
        self.settings_frame = self.tab.add("Settings")
        self.filters_frame = self.tab.add("Filters")
        self.configure()

    def configure(self):
        settings = Settings()

        MainFrame(settings, self.main_frame).initialize()
        SettingsFrame(settings,self.settings_frame).initialize()
        FilterFrame(settings, self.filters_frame).initialize()

if __name__ == "__main__":
    app = ctk.CTk()
    NeoFlixApp(app)
