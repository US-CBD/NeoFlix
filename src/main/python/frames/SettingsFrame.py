import sys
import threading
import time
import tkinter as tk

import customtkinter as ctk

from ..api.movies_by_genre import get_movies_by_genre
from ..api.top_movies import get_top_movies

try:
    from src.main.python.api.base import fetch_genre_ids, get_genre_names
    from src.main.python.frames.ScrollableFilmsFrames import ScrollableFilmsFrames
except ModuleNotFoundError:
    from .api.base import fetch_genre_ids
    from frames.ScrollableFilmsFrames import ScrollableFilmsFrames

class SettingsFrame:
    def __init__(self, settings, settings_frame):
        self.settings = settings
        self.settings_frame = settings_frame
        ###
        # TODO: Se deben de obtener desde la base de datos.
        fetch_genre_ids()
        self.genres = get_genre_names()
        self.favorites = [("a", "../../resources/placeholder.jpg"), ("b", "../../resources/placeholder.jpg"), ("c", "../../resources/placeholder.jpg")]
        self.genres_frame = None
        self.favorites_frame = None

    def initialize(self):
        self.genres_frame = ctk.CTkFrame(self.settings_frame)
        self.genres_frame.grid(row=0, column=0)
        genres_label = ctk.CTkLabel(self.genres_frame, text="Genres", fg_color="gray30", corner_radius=6)
        genres_label.grid(row=0, column=0)

        self.favorites_frame = ctk.CTkFrame(self.settings_frame)
        self.favorites_frame.grid(row=0, column=1)
        fav_label = ctk.CTkLabel(self.favorites_frame, text="Favourites", fg_color="gray30", corner_radius=6)
        fav_label.grid(row=0, column=0)

        self.configure()

    def configure(self):
        self.configure_genres()
        self.configure_favorites()
        self.configure_load_button()
        self.configure_console()

        self.settings_frame.after(1, self.add_logic)

    def configure_genres(self):


        scrollable_frame = ctk.CTkScrollableFrame(self.genres_frame)
        scrollable_frame.grid(row=1, column=0)

        self.checkboxes = []
        for i, genre in enumerate(self.genres):
            var = tk.IntVar()
            checkbox = ctk.CTkCheckBox(scrollable_frame, text=genre, variable=var)
            checkbox.grid(row=i + 1, column=0)
            self.checkboxes.append([genre, var])

    def configure_favorites(self):
        scrollable_films_frame = ScrollableFilmsFrames(self.favorites_frame, self.favorites)
        scrollable_films_frame.grid(row=1, column=0, sticky="ew")

    def configure_load_button(self):
        load_button = ctk.CTkButton(self.settings_frame, text="Load", corner_radius=6)
        load_button.grid(row=2, column=1)
        load_button.bind("<Button-1>", self.load_image)

    def configure_console(self):
        # Quiero un label con estilo de consolar que me permita ir poniendo mensajes de debug
        scrollable_frame = ctk.CTkScrollableFrame(self.settings_frame)
        scrollable_frame.grid(row=3, column=1, columnspan=3,
                              sticky="nsew")  # Ajusta la configuración sticky para ocupar todo el espacio disponible
        scrollable_frame.grid_rowconfigure(0, weight=1)  # Hacer que la fila 0 crezca con el cambio de tamaño
        scrollable_frame.grid_columnconfigure(0, weight=1)  # Hacer que la columna 0 crezca con el cambio de tamaño
        self.console = ctk.CTkTextbox(scrollable_frame, font=("Console", 12), fg_color="gray30", corner_radius=6)
        self.console.pack(fill="both", expand=True)
        console_redirector = ConsoleRedirector(self.console)
        sys.stdout = console_redirector
        self.update = False

    def load_image(self, event):
        threading.Thread(target=self.update_images).start()


    def add_logic(self):
        for genre, var in self.checkboxes:
            if self.settings.check_genre(genre) and not var.get():
                self.settings.remove_genre(genre)
            elif not self.settings.check_genre(genre) and var.get():
                self.settings.add_genre(genre)
        self.settings_frame.after(500, self.add_logic)

    def update_images(self):
        start = time.time()
        print("==Loading movies==")

        for genre, var in self.checkboxes:
            if var.get():
                print(f"==Loading movies for {genre}==")
                get_movies_by_genre(genre)
        print("==Loading top movies==")
        get_top_movies()
        print("==Loading complete==")
        print(f"==Elapsed time: {time.time() - start}==")
        self.settings.update = True

class ConsoleRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert(tk.END, text)

    def flush(self):
        pass


