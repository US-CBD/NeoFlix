import os
from configparser import ConfigParser

import customtkinter as ctk

from src.main.python.api.base import initialize_tmdb
from src.main.python.frames.filter_frame import FilterFilmFrame, FilterPersonFrame
from src.main.python.frames.main_frame import MainFrame
from src.main.python.frames.settings_frame import SettingsFrame
from src.main.python.models.models import Film
from src.main.python.settings import Settings


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
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.ini")
        config.read(config_path)
        token = config.get("TMDB", "password")
        initialize_tmdb(token)

        self.tab = ctk.CTkTabview(self.app)
        self.tab.pack(fill="both", expand=True)
        self.main_frame = self.tab.add("Main")
        self.settings_frame = self.tab.add("Settings")
        self.filter_film_frame = self.tab.add("Filter Film")
        # self.filter_person_frame = self.tab.add("Filter Person")
        self.configure()

    def configure(self):
        settings = Settings()
        MainFrame(settings, self.main_frame).initialize()
        SettingsFrame(settings, self.settings_frame).initialize()
        FilterFilmFrame(self.filter_film_frame, settings).initialize()
        # FilterPersonFrame(self.filter_person_frame, settings).initialize()


if __name__ == "__main__":
    app = ctk.CTk()
    NeoFlixApp(app)
