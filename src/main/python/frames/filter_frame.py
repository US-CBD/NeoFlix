import tkinter as tk

import customtkinter as ctk

from src.main.python.frames.list_film_frames import ListFilmsFrames
from src.main.python.models.models import Film


class FilterFrame:
    def __init__(self, settings, filter_frame):
        self.settings = settings
        self.filter_frame = filter_frame
        self.genres = []
        self.fav = []
        

    def initialize(self):
        # Crea un frame para los filtros
        top_frame = ctk.CTkFrame(self.filter_frame)
        top_frame.pack(fill="x")

        # Crea el dropdown button
        self.filter_option = tk.StringVar()
        self.filter_option.set("filter")
        dropdown_button = ctk.CTkButton(top_frame, textvariable=self.filter_option, command=self.open_menu)
        dropdown_button.grid(row=0, column=1)

        # Crea el search bar
        self.search_var = tk.StringVar()
        search_bar = ctk.CTkEntry(top_frame, textvariable=self.search_var)
        search_bar.grid(row=0, column=2)
        self.search_var.trace("w", self.filter_films)


        scrollable_frame = ctk.CTkScrollableFrame(self.filter_frame)
        scrollable_frame.pack(fill="both", expand=True)

        # Crea el dropdown menu
        self.dropdown_menu = ctk.CTkFrame(top_frame)
        for option in ["filter", "actor", "director", "film", "genre"]:
            button = ctk.CTkButton(self.dropdown_menu, text=option, command=lambda option=option: self.select_option(option))
            button.pack()

        self.films_frames = [("Filtro", ctk.CTkFrame(scrollable_frame),
                      Film.find_all())]
        self.configure()

    def open_menu(self):
        # Abre el menu de opciones
        self.dropdown_menu.grid(row=1, column=1)

    def select_option(self, option):
        # Selecciona la opcion
        self.filter_option.set(option)
        self.dropdown_menu.grid_forget() 

    def filter_films(self, *args):
        filter_option = self.filter_option.get()
        search_text = self.search_var.get()

        if filter_option == "film":
            films = Film.contain_by_title(search_text)
        elif filter_option == "actor":
            films = Film.contain_by_actor(search_text)
        elif filter_option == "director":
            films = Film.contain_by_director(search_text)
        elif filter_option == "genre":
            films = Film.contain_by_genre(search_text)
        else:
            films = Film.find_all()

        # Call update_films on each AllFilmsFrames object in the list
        for all_films_frame in self.all_films_frame:
            all_films_frame.update_films(films)
    def configure(self):
        self.filter_frame.grid_rowconfigure(0, weight=1)
        self.filter_frame.grid_columnconfigure(0, weight=1)

        self.all_films_frame = []
        for i, (title, frame, films) in enumerate(self.films_frames):
            frame.grid(row=i, column=0, sticky="ew")
            title = ctk.CTkLabel(frame, text=title, fg_color="gray30", corner_radius=6)
            title.grid(row=0, column=0)
            all_films_frame = ListFilmsFrames(frame, films, self.settings, width=700, height=150, size=(100, 100))
            all_films_frame.grid(row=1, column=0, sticky="nsew")
            self.all_films_frame.append(all_films_frame)
