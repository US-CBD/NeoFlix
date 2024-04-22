from typing import List, Tuple

import customtkinter as ctk

from src.main.python.frames.cards import CardFilmFrame
from src.main.python.models.models import Film
from src.main.python.settings import Settings


class ScrollableFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame: ctk.CTkFrame, films: List[Film], settings: Settings, width: int = 500, height: int = 150, size: Tuple[int, int] = (100, 100), *args, **kwargs) -> None:
        """
        Initializes a ScrollableFilmsFrames object.

        Args:
            parent_frame (ctk.CTkFrame): The parent frame.
            films (List[Film]): The list of films.
            settings (Any): The settings.
            width (int, optional): The width of the scrollable frame. Defaults to 500.
            height (int, optional): The height of the scrollable frame. Defaults to 150.
            size (Tuple[int, int], optional): The size of the films. Defaults to (100, 100).
        """
        super().__init__(parent_frame, *args, **kwargs)
        self.films = films
        self.settings = settings
        self.width = width
        self.height = height
        self.size = size
        self.initialize()

    def initialize(self) -> None:
        """Initializes the scrollable films frames."""
        scrollable_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", width=self.width, height=self.height)
        scrollable_frame.grid(row=1, column=0, sticky="ew")

        for i, film in enumerate(self.films):
            CardFilmFrame(scrollable_frame, film, self.settings, 0, i, self.size)

    def update_films(self, films: List[Film]) -> None:
        """
        Updates the films in the frame.

        Args:
            films (List[Film]): The updated list of films.
        """
        # Remove all current films from the frame
        for widget in self.winfo_children():
            widget.destroy()
        self.films = films
        self.initialize()

