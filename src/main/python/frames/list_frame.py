import customtkinter as ctk

from src.main.python.frames.cards import CardFilmFrame, CardPersonFrame


class ListFrames(ctk.CTkScrollableFrame):
    def __init__(self, parent_frame, items, item_type, settings, num_columns=4, size=(100, 100), *args, **kwargs):
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

    def initialize(self):
        start = self.page_number * self.items_per_page
        end = start + self.items_per_page
        for i, item in enumerate(self.items[start:end]):
            row = i // self.num_columns
            column = i % self.num_columns

            self.get_card_frame(item, row, column)

        next_button = ctk.CTkButton(self, text="Next", command=self.next_page)
        next_button.grid(row=self.num_columns + 1, column=1)

        previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_page)
        previous_button.grid(row=self.num_columns + 1, column=2)

    def get_card_frame(self, item, row, column):
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, items):
        # Remove all current items from the frame
        for widget in self.winfo_children():
            widget.destroy()
        self.items = items
        self.initialize()

    def next_page(self):
        if(not (self.page_number * self.items_per_page > len(self.items))):
            self.page_number += 1
            self.update(self.items)

    def previous_page(self):
        self.page_number = max(0, self.page_number - 1)
        self.update(self.items)


class ListFilmsFrames(ListFrames):
    def __init__(self, parent_frame, films, settings, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, films, 'film', settings, num_columns, size, *args, **kwargs)

    def get_card_frame(self, film, row, column):
        CardFilmFrame(self, film, self.settings, row, column, self.size)


class ListPersonsFrames(ListFrames):
    def __init__(self, parent_frame, persons, settings, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, persons, 'person', settings, num_columns, size, *args, **kwargs)

    def get_card_frame(self, person, row, column):
        CardPersonFrame(self, person, self.settings, row, column, self.size)