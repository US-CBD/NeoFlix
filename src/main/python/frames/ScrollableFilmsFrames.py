import customtkinter as ctk

from src.main.python.frames.cards.CardFilmFrame import CardFilmFrame


class ScrollableFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame, films,settings, width=500, height=150, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.films = films
        self.settings = settings
        self.width = width
        self.height = height
        self.size = size
        self.initialize()

    def initialize(self):
        scrollable_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", width=self.width, height=self.height)
        scrollable_frame.grid(row=1, column=0, sticky="ew")

        for i, film in enumerate(self.films):
            CardFilmFrame(scrollable_frame, film, self.settings, 0, i, self.size)
