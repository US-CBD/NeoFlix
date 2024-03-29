import os
from configparser import ConfigParser

import customtkinter as ctk

from src.main.python.api.base import initialize_tmdb

try:
    from src.main.python.Settings import Settings
    from src.main.python.frames.FilterFrame import FilterFrame
    from src.main.python.frames.MainFrame import MainFrame
    from src.main.python.frames.SettingsFrame import SettingsFrame
except ModuleNotFoundError:
    from Settings import Settings
    from frames.FilterFrame import FilterFrame
    from frames.MainFrame import MainFrame
    from frames.SettingsFrame import SettingsFrame


class NeoFlixApp:
    def __init__(self, app):
        self.app = app
        self.app.title("NeoFlix")
        self.app.geometry("800x600")
        self.app.configure(bg="black")
        self.app.resizable(False, False)
        # Get the current file's directory
        current_dir = os.path.dirname(os.path.realpath(__file__))
        favicon_path = os.path.join(current_dir, '..', 'resources', 'favicon.ico')
        self.app.iconbitmap(favicon_path)
        self.initialize()
        self.app.mainloop()

    def initialize(self):
        config = ConfigParser()
        config.read("config.ini")
        token = config.get("TMDB", "password")
        initialize_tmdb(token)

        self.tab = ctk.CTkTabview(self.app)
        self.tab.pack(fill="both", expand=True)
        self.main_frame =self.tab.add("Main")
        self.settings_frame = self.tab.add("Settings")
        self.filters_frame = self.tab.add("Filters")
        self.configure()

    def configure(self):
        settings = Settings()
        print("Hola")
        MainFrame(settings, self.main_frame).initialize()
        SettingsFrame(settings,self.settings_frame).initialize()
        FilterFrame(settings, self.filters_frame).initialize()

if __name__ == "__main__":
    app = ctk.CTk()
    NeoFlixApp(app)
