import os
from PIL import Image

import customtkinter as ctk
import tkinter as tk

from src.main.python.frames.ScrollableFilmsFrames import ScrollableFilmsFrames


class SettingsFrame:
    def __init__(self, settings, settings_frame):
        self.settings = settings
        self.settings_frame = settings_frame
        ###
        # TODO: Se deben de obtener desde la base de datos.
        self.genres = ["a", "b", "c"]
        self.favorites = [("a", "../../resources/placeholder.jpg"), ("b", "../../resources/placeholder.jpg"), ("c", "../../resources/placeholder.jpg")]
        ###
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

    def load_image(self, event):
        pass

    def add_logic(self):
        for genre, var in self.checkboxes:
            ###
            # TODO: Comporbar si se el estado en el usaurio
            print(var.get())
            # Si ya lo poseía y ha sido seleccionado como 1, no se hace nada.
            # Si no lo poseía y ha sido seleccionado como 1, se añade a la base de datos.
            # Si lo poseía y ha sido seleccionado como 0, se elimina de la base de datos.
            # Si no lo poseía y ha sido seleccionado como 0, no se hace nada.
            ###
        self.settings_frame.after(500, self.add_logic)


