from typing import Tuple

import customtkinter as ctk

from src.main.python.frames.cards import CardFilmFrame
from src.main.python.frames.list_frame import ListFrames
from src.main.python.models.models import Film
from src.main.python.settings import Settings


class FilmsWithGenreFrames(ListFrames):
    def __init__(self, parent_frame: ctk.CTkFrame, genre: str, settings: Settings, num_columns: int = 4, size: Tuple[int, int] = (100, 100), *args, **kwargs) -> None:
        """
        Initializes a ListFilmsFrames object.

        Args:
            parent_frame (ctk.CTkFrame): The parent frame.
            genre (str): The genre of the films.
            settings (Any): The settings for the frame.
            num_columns (int, optional): The number of columns. Defaults to 4.
            size (Tuple[int, int], optional): The size of each item. Defaults to (100, 100).
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        films = Film.find_by_genre(genre.capitalize())
        super().__init__(parent_frame, films, 'film', settings, num_columns, size, *args, **kwargs)

    def get_card_frame(self, film: Film, row: int, column: int) -> None:
        """Gets the card frame for a film."""
        CardFilmFrame(self, film, self.settings, row, column, self.size)
