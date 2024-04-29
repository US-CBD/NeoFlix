from typing import List, Any, Tuple

import customtkinter as ctk

from src.main.python.frames.cards import CardFilmFrame, CardPersonFrame
from src.main.python.models.models import Worker, Film
from src.main.python.settings import Settings


class ListFrames(ctk.CTkScrollableFrame):
    def __init__(self, parent_frame: ctk.CTkFrame, items: List[Any], item_type: str, settings: Any, num_columns: int = 4, size: Tuple[int, int] = (100, 100), *args, **kwargs) -> None:
        """
        Initializes a ListFrames object.

        Args:
            parent_frame (ctk.CTkFrame): The parent frame.
            items (List[Any]): The list of items.
            item_type (str): The type of item.
            settings (Any): The settings for the frame.
            num_columns (int, optional): The number of columns. Defaults to 4.
            size (Tuple[int, int], optional): The size of each item. Defaults to (100, 100).
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(parent_frame, *args, **kwargs)
        self.items = items
        self.num_columns = num_columns
        self.size = size
        self.settings = settings
        self.item_type = item_type
        self.grid(sticky="nsew")

        # Add pagination attributes
        self.page_number = 0
        self.items_per_page = num_columns * 2  # Adjust this value as needed

        self.initialize()

    def initialize(self) -> None:
        """Initializes the ListFrames."""
        start = self.page_number * self.items_per_page
        end = start + self.items_per_page
        for i, item in enumerate(self.items[start:end]):
            row = i // self.num_columns
            column = i % self.num_columns

            self.get_card_frame(item, row, column)

        previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_page)
        previous_button.grid(row=self.num_columns + 1, column=1)

        next_button = ctk.CTkButton(self, text="Next", command=self.next_page)
        next_button.grid(row=self.num_columns + 1, column=2)



    def get_card_frame(self, item: Any, row: int, column: int) -> None:
        """Gets the card frame."""
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, items: List[Any]) -> None:
        """
        Updates the list frame.

        Args:
            items (List[Any]): The updated list of items.
        """
        # Remove all current items from the frame
        for widget in self.winfo_children():
            widget.destroy()
        self.items = items
        self.initialize()

    def next_page(self) -> None:
        """Goes to the next page."""
        if not (self.page_number * self.items_per_page > len(self.items)):
            self.page_number += 1
            self.update(self.items)

    def previous_page(self) -> None:
        """Goes to the previous page."""
        self.page_number = max(0, self.page_number - 1)
        self.update(self.items)


class ListFilmsFrames(ListFrames):
    def __init__(self, parent_frame: ctk.CTkFrame, films: List[Film], settings: Settings, num_columns: int = 4, size: Tuple[int, int] = (100, 100), *args, **kwargs) -> None:
        """
        Initializes a ListFilmsFrames object.

        Args:
            parent_frame (ctk.CTkFrame): The parent frame.
            films (List[Film]): The list of films.
            settings (Any): The settings for the frame.
            num_columns (int, optional): The number of columns. Defaults to 4.
            size (Tuple[int, int], optional): The size of each item. Defaults to (100, 100).
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(parent_frame, films, 'film', settings, num_columns, size, *args, **kwargs)

    def get_card_frame(self, film: Film, row: int, column: int) -> None:
        """Gets the card frame for a film."""
        CardFilmFrame(self, film, self.settings, row, column, self.size)




class ListPersonsFrames(ListFrames):
    def __init__(self, parent_frame: ctk.CTkFrame, persons: List[Worker], settings: Settings, num_columns: int = 4, size: Tuple[int, int] = (100, 100), *args, **kwargs) -> None:
        """
        Initializes a ListPersonsFrames object.

        Args:
            parent_frame (ctk.CTkFrame): The parent frame.
            persons (List[Worker]): The list of workers.
            settings (Settings): The settings for the frame.
            num_columns (int, optional): The number of columns. Defaults to 4.
            size (Tuple[int, int], optional): The size of each item. Defaults to (100, 100).
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(parent_frame, persons, 'person', settings, num_columns, size, *args, **kwargs)

    def get_card_frame(self, person: Worker, row: int, column: int) -> None:
        """Gets the card frame for a person."""
        CardPersonFrame(self, person, self.settings, row, column, self.size)
