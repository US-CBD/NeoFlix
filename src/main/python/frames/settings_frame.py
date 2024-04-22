import sys
import threading
import time
import tkinter as tk

import customtkinter as ctk

from src.main.python.api.base import fetch_genre_ids, get_genre_names
from src.main.python.api.movies_by_genre import get_movies_by_genre
from src.main.python.api.top_movies import get_top_movies
from src.main.python.frames.scrollable_films_frames import ScrollableFilmsFrames
from src.main.python.settings import Settings


class SettingsFrame:
    def __init__(self, settings: Settings, settings_frame: ctk.CTkFrame) -> None:
        """
        Initializes a SettingsFrame object.

        Args:
            settings (Settings): The settings.
            settings_frame (ctk.CTkFrame): The settings frame.
        """
        self.settings = settings
        self.settings_frame = settings_frame
        fetch_genre_ids()
        self.genres = get_genre_names()
        self.favourites = self.settings.user.get_favorite_films()
        self.genres_frame = None
        self.favourites_frame = None

    def initialize(self) -> None:
        """Initializes the settings frame."""
        self.genres_frame = ctk.CTkFrame(self.settings_frame)
        self.genres_frame.grid(row=0, column=0)
        genres_label = ctk.CTkLabel(self.genres_frame, text="Genres", fg_color="gray30", corner_radius=6)
        genres_label.grid(row=0, column=0)

        self.favourites_frame = ctk.CTkFrame(self.settings_frame)
        self.favourites_frame.grid(row=0, column=1)
        fav_label = ctk.CTkLabel(self.favourites_frame, text="Favourites", fg_color="gray30", corner_radius=6)
        fav_label.grid(row=0, column=0)

        self.configure()

    def configure(self) -> None:
        """Configures the settings frame."""
        self.configure_genres()
        self.configure_favorites()
        self.configure_load_button()
        self.configure_console()

        self.settings_frame.after(1, self.add_logic)

    def configure_genres(self) -> None:
        """Configures the genres."""
        scrollable_frame = ctk.CTkScrollableFrame(self.genres_frame)
        scrollable_frame.grid(row=1, column=0)

        self.checkboxes = []
        for i, genre in enumerate(self.genres):
            var = tk.IntVar()
            checkbox = ctk.CTkCheckBox(scrollable_frame, text=genre, variable=var)
            checkbox.grid(row=i + 1, column=0)
            self.checkboxes.append([genre, var])

    def configure_favorites(self) -> None:
        """Configures the favorites."""
        self.scrollable_films_frame = ScrollableFilmsFrames(self.favourites_frame, self.favourites, self.settings)
        self.scrollable_films_frame.grid(row=1, column=0, sticky="ew")

    def configure_load_button(self) -> None:
        """Configures the load button."""
        load_button = ctk.CTkButton(self.settings_frame, text="Load", corner_radius=6)
        load_button.grid(row=2, column=1)
        load_button.bind("<Button-1>", self.load_up)

    def configure_console(self) -> None:
        """Configures the console."""
        self.console = ctk.CTkTextbox(self.settings_frame, font=("Console", 12), fg_color="gray30", corner_radius=6)
        self.console.grid(columnspan=2, sticky="ew")
        self.console_redirector = ConsoleRedirector(self.console)
        sys.stdout = self.console_redirector
        self.update = False
        self.settings_frame.after(500, self.add_logic)

    def load_up(self, event) -> None:
        """Loads data from the database."""
        threading.Thread(target=self.update_db).start()

    def add_logic(self) -> None:
        """Adds logic to the settings."""
        for genre, var in self.checkboxes:
            if self.settings.check_genre(genre) and not var.get():
                self.settings.remove_genre(genre)
                self.settings.update_main = True
            elif not self.settings.check_genre(genre) and var.get():
                self.settings.add_genre(genre)
                self.settings.update_main = True
        if self.settings.update_favourites:
            self.favourites = self.settings.user.get_favorite_films()
            self.scrollable_films_frame.update_films(self.favourites)
            self.settings.update_favourites = False
        self.settings_frame.after(500, self.add_logic)

    def update_db(self) -> None:
        """Updates the database."""
        self.console_redirector.clean()
        start = time.time()
        print("==Loading movies==")
        print("==Loading top movies==")
        get_top_movies()
        print("==Top movies loaded==")
        for genre, var in self.checkboxes:
            if var.get():
                print(f"==Loading movies for {genre}==")
                get_movies_by_genre(genre)

        print("==Loading complete==")
        print(f"==Elapsed time: {time.time() - start}==")
        self.settings.update_main = True


class ConsoleRedirector:
    def __init__(self, textbox: ctk.CTkTextbox) -> None:
        """
        Initializes a ConsoleRedirector object.

        Args:
            textbox (ctk.CTkTextbox): The console textbox.
        """
        self.textbox = textbox

    def write(self, text: str) -> None:
        """Writes text to the console textbox."""
        self.textbox.insert(tk.END, text)

    def flush(self) -> None:
        """Flushes the buffer."""
        pass

    def clean(self) -> None:
        """Cleans all the text in the console."""
        self.textbox.delete("1.0", tk.END)



