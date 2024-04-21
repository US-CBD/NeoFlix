import tkinter as tk

import customtkinter as ctk

from src.main.python.frames.list_frame import ListFilmsFrames, ListPersonsFrames
from src.main.python.models.models import Film, Worker


class FilterFrame(ctk.CTkFrame):
    def __init__(self, parent_frame, settings, filter_options, filter_functions, *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.items = filter_functions['default']()
        self.settings = settings
        self.filter_options = filter_options
        self.filter_functions = filter_functions
        self.grid(sticky="nsew")
        self.initialize()

    def initialize(self):
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=0, column=0, sticky="nsew")

        filter_option = tk.StringVar()
        # Ensure all options are converted to strings
        filter_option = tk.StringVar()
        filter_option.set(self.filter_options[0])  # Default to the first option
        filter_dropdown = ctk.CTkOptionMenu(filter_frame, variable=filter_option, values=self.filter_options)

        filter_dropdown.grid(row=0, column=0, padx=5, pady=5)

        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(filter_frame, textvariable=search_var)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        search_var.trace("w", lambda *args: self.filter_items(filter_option.get(), search_var.get()))

        self.list_items_frame = self.get_list_frame()
        self.list_items_frame.grid(row=1, column=0, sticky="nsew")

    def filter_items(self, filter_by, search_text):
        filtered_items = []

        if filter_by in self.filter_functions:
            filtered_items = self.filter_functions[filter_by](search_text)
        else:
            filtered_items = self.filter_functions['default']()

        self.list_items_frame.update(filtered_items)

    def get_list_frame(self):
        raise NotImplementedError("Subclasses must implement this method")


class FilterFilmFrame(FilterFrame):
    def __init__(self, parent_frame, settings, *args, **kwargs):
        filter_options = ["Filter by", "Title", "Actor", "Director", "Genre"]
        filter_functions = {
            "Title": Film.contain_by_title,
            "Actor": Film.contain_by_actor,
            "Director": Film.contain_by_director,
            "Genre": Film.contain_by_genre,
            "default": Film.find_all
        }
        super().__init__(parent_frame, settings, filter_options, filter_functions, *args, **kwargs)

    def get_list_frame(self):
        return ListFilmsFrames(self, self.items, self.settings, width=780, height=500, size=(100, 100))


class FilterPersonFrame(FilterFrame):
    def __init__(self, parent_frame, settings, *args, **kwargs):
        filter_options = ["Filter by", "Name", "Acted in", "Directed by"]
        filter_functions = {
            "Name": Worker.find,
            "Acted in": Film.get_actors_for_film,
            "Directed by": Film.get_directors_for_film,
            "default": Worker.find_all
        }
        super().__init__(parent_frame, settings, filter_options, filter_functions, *args, **kwargs)

    def get_list_frame(self):
        return ListPersonsFrames(self, self.items, self.settings, width=700, height=150, size=(100, 100))





