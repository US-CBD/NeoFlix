import os
from typing import Any, Callable, Type, Tuple

import PIL.Image
import customtkinter as ctk
from PIL.Image import Image
from customtkinter import CTkFrame

from src.main.python.frames.details import DetailsFilmFrame, DetailsPersonFrame
from src.main.python.models.base import Base
from src.main.python.models.models import Worker, Film
from src.main.python.settings import Settings


class CardFrame:
    def __init__(self, parent_frame: CTkFrame, item: Base, settings: Settings, row: int, column: int, size: Tuple[int, int],
                 title_attribute: str, image_path_method: Callable[[Any], str],
                 details_frame_class: Type[Any]) -> None:
        """
        Initializes a CardFrame object.

        Args:
            parent_frame (CTkFrame): The parent frame.
            item (Base): The item to display.
            settings (Settings): The settings for the frame.
            row (int): The row position.
            column (int): The column position.
            size (Tuple[int, int]): The size of the image.
            title_attribute (str): The attribute of the item to be used as title.
            image_path_method (Callable[[Any], str]): The method to get the image path for the item.
            details_frame_class (Type[Any]): The class of the details frame.
        """
        self.parent_frame = parent_frame
        self.item = item
        self.settings = settings
        self.row = row
        self.column = column
        self.size = size
        self.title_attribute = title_attribute
        self.image_path_method = image_path_method
        self.details_frame_class = details_frame_class
        self.initialize()

    def initialize(self) -> None:
        """
        Initializes the CardFrame.
        """
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.image_path_method(self.item))
        try:
            image = ctk.CTkImage(PIL.Image.open(image_path), size=self.size)
        except PIL.UnidentifiedImageError:
            image = ctk.CTkImage(PIL.Image.new("RGB", self.size, "gray"), size=self.size)

        button = ctk.CTkButton(self.parent_frame, text=getattr(self.item, self.title_attribute), image=image,
                               command=self.show_detail_frame, compound="top")
        button.grid(row=self.row, column=self.column)

    def show_detail_frame(self) -> None:
        """
        Shows the detail frame for the item.
        """
        self.details_frame_class(self.item, self.settings)

class CardFilmFrame(CardFrame):
    def __init__(self, parent_frame: CTkFrame, film: Film, settings: Settings, row: int, column: int, size: Tuple[int, int]) -> None:
        """
        Initializes a CardFilmFrame object.

        Args:
            parent_frame (CTkFrame): The parent frame.
            film (Film): The film object.
            settings (Settings): The settings for the frame.
            row (int): The row position.
            column (int): The column position.
            size (Tuple[int, int]): The size of the image.
        """
        super().__init__(parent_frame, film, settings, row, column, size, 'title', lambda film: film.get_path(),
                         DetailsFilmFrame)

class CardPersonFrame(CardFrame):
    def __init__(self, parent_frame: CTkFrame, person: Worker, settings: Settings, row: int, column: int, size: Tuple[int, int]) -> None:
        """
        Initializes a CardPersonFrame object.

        Args:
            parent_frame (CTkFrame): The parent frame.
            person (Worker): The person object.
            settings (Settings): The settings for the frame.
            row (int): The row position.
            column (int): The column position.
            size (Tuple[int, int]): The size of the image.
        """
        super().__init__(parent_frame, person, settings, row, column, size, 'name', lambda person: person.get_path(),
                         DetailsPersonFrame)

