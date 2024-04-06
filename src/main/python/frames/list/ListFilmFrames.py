import customtkinter as ctk

try:
    from src.main.python.frames.cards.CardFilmFrame import CardFilmFrame
except ModuleNotFoundError:
    from frames.cards.CardFilmFrame import CardFilmFrame

class AllFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame, films, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.films = films
        self.num_columns = num_columns
        self.size = size
        self.grid(sticky="nsew")
        self.initialize()

    def initialize(self):
        for i, film in enumerate(self.films):
            row = i // self.num_columns
            column = i % self.num_columns

            CardFilmFrame(self, film, row, column, self.size)


    def update_films(self, filtered_film):
        # Remove all current films from the frame
        for widget in self.winfo_children():
            widget.destroy()
        self.films = filtered_film
        self.initialize()
