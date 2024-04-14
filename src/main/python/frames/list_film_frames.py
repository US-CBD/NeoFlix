import customtkinter as ctk

from src.main.python.frames.cards import CardFilmFrame


class ListFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame, films, settings, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.films = films
        self.num_columns = num_columns
        self.size = size
        self.settings = settings
        self.grid(sticky="nsew")
        self.initialize()

    def initialize(self):
        for i, film in enumerate(self.films):
            row = i // self.num_columns
            column = i % self.num_columns

            CardFilmFrame(self, film, self.settings, row, column, self.size)


    def update_films(self, filtered_film):
        # Remove all current films from the frame
        for widget in self.winfo_children():
            widget.destroy()
        self.films = filtered_film
        self.initialize()
